import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QLineEdit, QSpinBox, QComboBox,
                           QPushButton, QRadioButton, QButtonGroup, QGroupBox,
                           QScrollArea)
from PyQt5.QtCore import Qt
import os
import sys
sys.path.append('../Funciones')  # Update path to point to Funciones directory
from pajarito import scrape_twitter
from generarcsv import process_tweet_file

class TwitterScraperGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Twitter Advanced Search')
        self.setMinimumWidth(800)
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        # Words section
        words_group = QGroupBox("Words")
        words_layout = QVBoxLayout()
        
        # All of these words
        self.all_words = QLineEdit()
        words_layout.addWidget(QLabel("All of these words"))
        words_layout.addWidget(self.all_words)
        
        # This exact phrase
        self.exact_phrase = QLineEdit()
        words_layout.addWidget(QLabel("This exact phrase"))
        words_layout.addWidget(self.exact_phrase)
        
        # Any of these words
        self.any_words = QLineEdit()
        words_layout.addWidget(QLabel("Any of these words"))
        words_layout.addWidget(self.any_words)
        
        # None of these words
        self.none_words = QLineEdit()
        words_layout.addWidget(QLabel("None of these words"))
        words_layout.addWidget(self.none_words)
        
        # These hashtags
        self.hashtags = QLineEdit()
        words_layout.addWidget(QLabel("These hashtags"))
        words_layout.addWidget(self.hashtags)
        
        words_group.setLayout(words_layout)
        scroll_layout.addWidget(words_group)
        
        # Accounts section
        accounts_group = QGroupBox("Accounts")
        accounts_layout = QVBoxLayout()
        
        # From these accounts
        self.from_accounts = QLineEdit()
        accounts_layout.addWidget(QLabel("From these accounts"))
        accounts_layout.addWidget(self.from_accounts)
        
        # To these accounts
        self.to_accounts = QLineEdit()
        accounts_layout.addWidget(QLabel("To these accounts"))
        accounts_layout.addWidget(self.to_accounts)
        
        # Mentioning these accounts
        self.mentioning = QLineEdit()
        accounts_layout.addWidget(QLabel("Mentioning these accounts"))
        accounts_layout.addWidget(self.mentioning)
        
        accounts_group.setLayout(accounts_layout)
        scroll_layout.addWidget(accounts_group)
        
        # Engagement section
        engagement_group = QGroupBox("Engagement")
        engagement_layout = QVBoxLayout()
        
        # Minimum replies
        self.min_replies = QSpinBox()
        self.min_replies.setMaximum(999999999)
        engagement_layout.addWidget(QLabel("Minimum replies"))
        engagement_layout.addWidget(self.min_replies)
        
        # Minimum likes
        self.min_likes = QSpinBox()
        self.min_likes.setMaximum(999999999)
        engagement_layout.addWidget(QLabel("Minimum likes"))
        engagement_layout.addWidget(self.min_likes)
        
        # Minimum retweets
        self.min_retweets = QSpinBox()
        self.min_retweets.setMaximum(999999999)
        engagement_layout.addWidget(QLabel("Minimum retweets"))
        engagement_layout.addWidget(self.min_retweets)
        
        engagement_group.setLayout(engagement_layout)
        scroll_layout.addWidget(engagement_group)
        
        # Language section
        language_group = QGroupBox("Language")
        language_layout = QVBoxLayout()
        
        self.language = QComboBox()
        self.language.addItems(['Any language', 'English', 'Spanish', 'French', 'German', 
                              'Italian', 'Portuguese', 'Japanese', 'Korean', 'Chinese'])
        language_layout.addWidget(self.language)
        
        language_group.setLayout(language_layout)
        scroll_layout.addWidget(language_group)
        
        # Sort order
        sort_group = QGroupBox("Sort By")
        sort_layout = QHBoxLayout()
        
        self.sort_top = QRadioButton("Top")
        self.sort_latest = QRadioButton("Latest")
        self.sort_top.setChecked(True)
        
        sort_layout.addWidget(self.sort_top)
        sort_layout.addWidget(self.sort_latest)
        
        sort_group.setLayout(sort_layout)
        scroll_layout.addWidget(sort_group)
        
        # Start scraping button
        self.start_button = QPushButton("Start Scraping")
        self.start_button.clicked.connect(self.start_scraping)
        scroll_layout.addWidget(self.start_button)
        
    def generate_search_url(self):
        query_parts = []
        
        # Add search terms
        if self.all_words.text():
            query_parts.append(self.all_words.text())
        if self.exact_phrase.text():
            query_parts.append(f'"{self.exact_phrase.text()}"')
        if self.any_words.text():
            words = self.any_words.text().split()
            query_parts.append(f'({" OR ".join(words)})')
        if self.none_words.text():
            words = self.none_words.text().split()
            query_parts.append(f'-{" -".join(words)}')
        if self.hashtags.text():
            tags = self.hashtags.text().split()
            query_parts.extend([f'#{tag.strip("#")}' for tag in tags])
            
        # Add account filters
        if self.from_accounts.text():
            query_parts.append(f'from:{self.from_accounts.text()}')
        if self.to_accounts.text():
            query_parts.append(f'to:{self.to_accounts.text()}')
        if self.mentioning.text():
            query_parts.append(f'@{self.mentioning.text()}')
            
        # Add engagement filters
        if self.min_replies.value() > 0:
            query_parts.append(f'min_replies:{self.min_replies.value()}')
        if self.min_likes.value() > 0:
            query_parts.append(f'min_faves:{self.min_likes.value()}')
        if self.min_retweets.value() > 0:
            query_parts.append(f'min_retweets:{self.min_retweets.value()}')
            
        # Add language filter
        if self.language.currentText() != 'Any language':
            lang_codes = {'English': 'en', 'Spanish': 'es', 'French': 'fr', 
                         'German': 'de', 'Italian': 'it', 'Portuguese': 'pt',
                         'Japanese': 'ja', 'Korean': 'ko', 'Chinese': 'zh'}
            query_parts.append(f'lang:{lang_codes[self.language.currentText()]}')
            
        # Build the URL
        query = ' '.join(query_parts)
        base_url = 'https://x.com/search?q='
        sort_param = '&f=live' if self.sort_latest.isChecked() else ''
        
        return f"{base_url}{query}&src=typed_query{sort_param}"
        
    def start_scraping(self):
        search_url = self.generate_search_url()
        print(f"Generated URL: {search_url}")
        
        # Update file paths to use the Archivos directory
        output_txt = '../Archivos/pagina_contenido.txt'
        output_csv = '../Archivos/tweets.csv'
        
        try:
            # Run the scraping process with updated file path
            scrape_twitter(search_url, output_txt)
            
            # Process the results with updated file paths
            process_tweet_file(output_txt, output_csv)
            
            print(f'Scraping completed successfully. Results saved to {output_csv}')
        except Exception as e:
            print(f"Error during scraping: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = TwitterScraperGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()