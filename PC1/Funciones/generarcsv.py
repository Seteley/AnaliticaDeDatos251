import csv
from datetime import datetime
import re
import os

def parse_number(value):
    """Convert string numbers with K/M suffix to actual numbers."""
    if isinstance(value, str):
        value = value.lower().strip()
        if 'k' in value:
            return int(float(value.replace('k', '')) * 1000)
        elif 'm' in value:
            return int(float(value.replace('m', '')) * 1000000)
    try:
        return int(value)
    except:
        return value

def extract_tweet_info(tweet_html):
    """Extract tweet information from a single tweet's HTML content."""
    tweet_info = {}
    
    # Extract account name (looking for the first text content after verified account icon)
    account_name_match = re.search(r'data-testid="User-Name"[^>]*>.*?<span[^>]*>([^<]+)</span>', tweet_html)
    if account_name_match:
        tweet_info['account_name'] = account_name_match.group(1).strip()
    
    # Extract username (looking for @ pattern)
    username_match = re.search(r'@([^<"\s]+)', tweet_html)
    if username_match:
        tweet_info['username'] = username_match.group(1).strip()
    
    # Extract tweet text - modified to capture all spans within tweetText
    tweet_text_parts = []
    tweet_text_section = re.search(r'data-testid="tweetText"[^>]*>(.*?)</div>', tweet_html, re.DOTALL)
    if tweet_text_section:
        # Find all text content within spans
        spans = re.finditer(r'<span[^>]*>([^<]+)</span>', tweet_text_section.group(1))
        for span in spans:
            tweet_text_parts.append(span.group(1).strip())
        
        # Join all parts with a space and normalize whitespace
        full_tweet = ' '.join(tweet_text_parts)
        # Replace multiple spaces and newlines with a single space
        full_tweet = ' '.join(full_tweet.split())
        tweet_info['tweet'] = full_tweet
    
    # Extract datetime
    datetime_match = re.search(r'datetime="([^"]+)"', tweet_html)
    if datetime_match:
        tweet_info['datetime'] = datetime_match.group(1).strip()
    
    # Extract metrics
    replies_match = re.search(r'(\d+)\s*Replies', tweet_html)
    if replies_match:
        tweet_info['comments'] = parse_number(replies_match.group(1))
    
    retweets_match = re.search(r'(\d+)\s*reposts', tweet_html)
    if retweets_match:
        tweet_info['retweets'] = parse_number(retweets_match.group(1))
    
    likes_match = re.search(r'(\d+[KMk]?)\s*Likes', tweet_html)
    if likes_match:
        tweet_info['likes'] = parse_number(likes_match.group(1))
    
    views_match = re.search(r'(\d+[KMk]?)\s*views', tweet_html)
    if views_match:
        tweet_info['views'] = parse_number(views_match.group(1))
    
    return tweet_info

def split_tweets(html_content):
    """Split HTML content into individual tweets."""
    # Split by article tags which typically contain individual tweets
    tweets = re.findall(r'<article[^>]*>.*?</article>', html_content, re.DOTALL)
    if not tweets:
        # Fallback: try splitting by tweet container divs
        tweets = re.findall(r'<div[^>]*data-testid="cellInnerDiv"[^>]*>.*?</div>', html_content, re.DOTALL)
    return tweets

def process_tweet_file(input_file, output_file):
    """
    Process the input file and generate a CSV file.
    
    Args:
        input_file (str): Path to the input file containing tweet HTML or text
        output_file (str): Path where to save the CSV output
    """
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Write headers
        writer.writerow([
            'Nombre de la cuenta',
            'Nombre de usuario',
            'Tweet',
            'Hora y fecha',
            'Numero de comentarios',
            'Numero de retweets',
            'Numero de likes',
            'Visualizaciones'
        ])
        
        # Read and process input file
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Check if content is HTML or plain text
            if '<div' in content:
                # Process as HTML - split into individual tweets
                tweets = split_tweets(content)
                for tweet_html in tweets:
                    tweet_info = extract_tweet_info(tweet_html)
                    if tweet_info:  # Only write if we found tweet information
                        writer.writerow([
                            tweet_info.get('account_name', ''),
                            tweet_info.get('username', ''),
                            tweet_info.get('tweet', ''),
                            tweet_info.get('datetime', ''),
                            tweet_info.get('comments', ''),
                            tweet_info.get('retweets', ''),
                            tweet_info.get('likes', ''),
                            tweet_info.get('views', '')
                        ])
            else:
                # Process as plain text - handle single tweet format
                tweet_info = {}
                current_tweet = {}
                for line in content.split('\n'):
                    line = line.strip()
                    if line.startswith('nombre de cuenta:'):
                        if current_tweet:  # If we have a previous tweet, write it
                            writer.writerow([
                                current_tweet.get('account_name', ''),
                                current_tweet.get('username', ''),
                                current_tweet.get('tweet', ''),
                                current_tweet.get('datetime', ''),
                                current_tweet.get('comments', ''),
                                current_tweet.get('retweets', ''),
                                current_tweet.get('likes', ''),
                                current_tweet.get('views', '')
                            ])
                        current_tweet = {}  # Start new tweet
                        current_tweet['account_name'] = line.split(':', 1)[1].strip()
                    elif line.startswith('nombre de usuario:'):
                        current_tweet['username'] = line.split(':', 1)[1].strip()
                    elif line.startswith('tweet:'):
                        current_tweet['tweet'] = line.split(':', 1)[1].strip()
                    elif line.startswith('fecha y hora:'):
                        current_tweet['datetime'] = line.split(':', 1)[1].strip()
                    elif line.startswith('numero de comentario:'):
                        current_tweet['comments'] = parse_number(line.split(':', 1)[1].strip())
                    elif line.startswith('numero de retweets:'):
                        current_tweet['retweets'] = parse_number(line.split(':', 1)[1].strip())
                    elif line.startswith('numero de likes:'):
                        current_tweet['likes'] = parse_number(line.split(':', 1)[1].strip())
                    elif line.startswith('numero de visualizaciones:'):
                        current_tweet['views'] = parse_number(line.split(':', 1)[1].strip())
                
                # Write the last tweet if exists
                if current_tweet:
                    writer.writerow([
                        current_tweet.get('account_name', ''),
                        current_tweet.get('username', ''),
                        current_tweet.get('tweet', ''),
                        current_tweet.get('datetime', ''),
                        current_tweet.get('comments', ''),
                        current_tweet.get('retweets', ''),
                        current_tweet.get('likes', ''),
                        current_tweet.get('views', '')
                    ])

if __name__ == "__main__":
    # Example usage
    input_file = '../Archivos/pagina_contenido.txt'
    output_file = '../Archivos/tweets.csv'
    process_tweet_file(input_file, output_file)
    print(f'CSV file has been generated successfully: {output_file}')