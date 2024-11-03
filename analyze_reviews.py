import pandas as pd
from textblob import TextBlob
import re

common_dishes = [
    "pizza", "burger", "pasta", "sushi", "salad", "steak", "tacos", "curry", 
    "sandwich", "soup", "noodles", "fried rice", "chicken wings", "fish and chips", 
    "shawarma", "kebab", "hot pot", "ramen", "dumplings", "pho", "paella", 
    "burrito", "nachos", "poke bowl", "sashimi", "tempura", "gyoza", "dim sum", 
    "lasagna", "risotto", "spaghetti carbonara", "spaghetti bolognese", "gnocchi", 
    "french fries", "onion rings", "mashed potatoes", "coleslaw", "nachos", 
    "hummus", "falafel", "tabbouleh", "dolma", "baklava", "moussaka", "tzatziki", 
    "paella", "tapas", "jamón ibérico", "churros", "tortilla española", "gazpacho", 
    "ramen", "sushi", "tempura", "udon", "yakitori", "tonkatsu", "okonomiyaki", 
    "kimchi", "bibimbap", "bulgogi", "tteokbokki", "kimchi jjigae", "ramen", 
    "pho", "bánh mì", "gỏi cuốn", "bún chả", "phở gà", "phở bò", "bún riêu", 
    "bánh xèo", "bánh cuốn", "chả giò", "bánh mì thịt nướng", "bún bò huế", "bánh canh", 
    "lẩu", "cơm tấm", "xôi gấc", "xôi xéo", "bánh bao", "chả giò", "nem rán", "hủ tiếu", 
    "bún bò Huế", "phở", "bánh mì", "bánh xèo", "gỏi cuốn", "chả giò", "bún riêu", 
    "lẩu", "cơm tấm", "xôi gấc", "xôi xéo", "bánh bao", "chả giò", "nem rán", "hủ tiếu", 
    "pasta", "pizza", "risotto", "lasagna", "spaghetti", "gnocchi", "cannelloni", 
    "ravioli", "tortellini", "arancini", "bruschetta", "panini", "focaccia", 
    "polenta", "ossobuco", "risotto alla Milanese", "spaghetti carbonara", 
    "spaghetti alla Bolognese", "pizza Margherita", "pizza Napoli", "pizza Diavola", 
    "pizza quattro formaggi", "pizza capricciosa", "pizza marinara", "pizza ai funghi", 
    "pizza salsiccia e friarielli", "pizza prosciutto e funghi", "pizza diavola", 
    "pizza quattro stagioni", "pizza alla marinara", "pizza bianca", "pizza al taglio", 
    "focaccia al rosmarino", "focaccia farcita", "panini al prosciutto e mozzarella", 
    "panini al salame", "panini al pomodoro e mozzarella", "panini al crudo di Parma", 
    "bruschetta al pomodoro", "bruschetta con funghi", "bruschetta con prosciutto", 
    "bruschetta con olive", "risotto alla milanese", "risotto ai funghi porcini", 
    "risotto alla zucca", "risotto al nero di seppia", "risotto alla pescatora", 
    "spaghetti carbonara", "spaghetti alla bolognese", "spaghetti aglio e olio", 
    "spaghetti alle vongole", "spaghetti alle vongole veraci", "spaghetti alle cozze", 
    "lasagna alla bolognese", "lasagna al forno", "lasagna verde", "lasagna bianca", 
    "gnocchi al pomodoro", "gnocchi alla sorrentina", "gnocchi alla romana", 
    "gnocchi alla salsiccia e funghi", "cannelloni al forno", "tortellini in brodo", 
    "tortellini alla panna", "tortellini al ragù", "arancini di riso", "arancini al ragù", 
    "arancini al burro e parmigiano", "arancini al nero di seppia", "polenta", 
    "polenta con ragù", "polenta con funghi", "polenta con salsiccia", "ossobuco alla milanese", 
    "saltimbocca alla romana", "cotoletta alla milanese", "scaloppine al limone", 
    "pasta alla carbonara", "pasta alla amatriciana", "pasta alla cacio e pepe", 
    "pasta alla norma", "pasta alla puttanesca", "pasta alla siciliana", "pasta alla sorrentina", 
    "pasta al pesto", "pasta al pomodoro", "pasta con le sarde", "pasta con le vongole", 
    "pasta con le cozze", "pasta alla norma", "pasta alla puttanesca", "pasta alla siciliana", 
    "pasta al pesto", "pasta al pomodoro", "pasta con le sarde", "pasta con le vongole", 
    "pasta con le cozze", "pizza margherita", "pizza napoletana", "pizza alla romana", 
    "pizza al taglio", "pizza bianca", "focaccia al rosmarino", "focaccia farcita", 
    "panini al prosciutto e mozzarella", "panini al salame", "panini al pomodoro e mozzarella", 
    "panini al crudo di Parma", "bruschetta al pomodoro", "bruschetta con funghi", 
    "bruschetta con prosciutto", "bruschetta con olive", "risotto alla milanese", 
    "risotto ai funghi porcini", "risotto alla zucca", "risotto al nero di seppia", 
    "risotto alla pescatora", "spaghetti carbonara", "spaghetti alla bolognese", 
    "spaghetti aglio e olio", "spaghetti alle vongole", "spaghetti alle vongole veraci", 
    "spaghetti alle cozze", "lasagna alla bolognese", "lasagna al forno", "lasagna verde", 
    "lasagna bianca", "gnocchi al pomodoro", "gnocchi alla sorrentina", "gnocchi alla romana", 
    "gnocchi alla salsiccia e funghi", "cannelloni al forno", "tortellini in brodo", 
    "tortellini alla panna", "tortellini al ragù", "arancini di riso", "arancini al ragù", 
    "arancini al burro e parmigiano", "arancini al nero di seppia", "polenta", 
    "polenta con ragù", "polenta con funghi", "polenta con salsiccia", "ossobuco alla milanese", 
    "saltimbocca alla romana", "cotoletta alla milanese", "scaloppine al limone", 
    "pasta alla carbonara", "pasta alla amatriciana", "pasta alla cacio e pepe", 
    "pasta alla norma", "pasta alla puttanesca", "pasta alla siciliana", "pasta alla sorrentina", 
    "pasta al pesto", "pasta al pomodoro", "pasta con le sarde", "pasta con le vongole", 
    "pasta con le cozze", "pizza margherita", "pizza napoletana", "pizza alla romana", 
    "pizza al taglio", "pizza bianca", "focaccia al rosmarino", "focaccia farcita", 
    "panini al prosciutto e mozzarella", "panini al salame", "panini al pomodoro e mozzarella", 
    "panini al crudo di Parma", "bruschetta al pomodoro", "bruschetta con funghi", 
    "bruschetta con prosciutto", "bruschetta con olive", "risotto alla milanese", 
    "risotto ai funghi porcini", "risotto alla zucca", "risotto al nero di seppia", 
    "risotto alla pescatora", "spaghetti carbonara", "spaghetti alla bolognese", 
    "spaghetti aglio e olio", "spaghetti alle vongole", "spaghetti alle vongole veraci", 
    "spaghetti alle cozze", "lasagna alla bolognese", "lasagna al forno", "lasagna verde", 
    "lasagna bianca", "gnocchi al pomodoro", "gnocchi alla sorrentina", "gnocchi alla romana", 
    "gnocchi alla salsiccia e funghi", "cannelloni al forno", "tortellini in brodo", 
    "tortellini alla panna", "tortellini al ragù", "arancini di riso", "arancini al ragù", 
    "arancini al burro e parmigiano", "arancini al nero di seppia", "polenta", 
    "polenta con ragù", "polenta con funghi", "polenta con salsiccia", "ossobuco alla milanese", 
    "saltimbocca alla romana", "cotoletta alla milanese", "scaloppine al limone", 
    "pasta alla carbonara", "pasta alla amatriciana", "pasta alla cacio e pepe",  "naan", "biryani", "samosa", "tandoori chicken", "tea","coffee", "tacos", "burrito", "nachos", "enchiladas", "quesadillas", "fajitas", "guacamole", "salsa", "tortilla chips", "sushi", "sashimi", "tempura", "gyoza", "ramen", "udon", "yakitori", "tonkatsu", "okonomiyaki", "sushi rolls","burger", "french fries", "onion rings", "milkshake", "kimchi", "bibimbap", "bulgogi", "tteokbokki", "kimchi jjigae","hot dog", "chicken nuggets", "steak", "salad","fried rice", "noodles", "dumplings", "ramen", "pho", "spring rolls", "chow mein", "kung pao chicken", "mapo tofu", "sweet and sour chicken"]

# Load review data

# Load the reviews data
def load_reviews(filename):
    try:
        df = pd.read_csv(filename)
        return df
    except Exception as e:
        print(f"Error loading file: {e}")
        return None

# Analyze review sentiment
def analyze_sentiment(review):
    return TextBlob(review).sentiment.polarity

# Extract mentioned dishes in reviews
def extract_dish_mentions(review):
    review = review.lower()
    mentioned_dishes = [dish for dish in common_dishes if dish in review]
    return ', '.join(mentioned_dishes) if mentioned_dishes else None

# Main function to analyze reviews and filter for positive sentiment
def analyze_positive_dishes():
    # Load reviews
    reviews_df = load_reviews('restaurant_reviews.csv')
    if reviews_df is not None:
        # Add sentiment score and extract dishes
        reviews_df['sentiment_score'] = reviews_df['Review Text'].apply(analyze_sentiment)
        reviews_df['mentioned_dishes'] = reviews_df['Review Text'].apply(extract_dish_mentions)
        
        # Filter for positive sentiment reviews and non-empty dish mentions
        positive_df = reviews_df[(reviews_df['sentiment_score'] > 0) & (reviews_df['mentioned_dishes'].notna())]
        
        # Group by restaurant and combine positive dishes into unique lists
        result_df = positive_df.groupby('Name')['mentioned_dishes'].apply(
            lambda x: ', '.join(set(', '.join(x).split(', ')))
        ).reset_index()
        
        # Display the results
        print(result_df)
        
        # Save to CSV if needed
        result_df.to_csv('positive_dishes_per_restaurant.csv', index=False)

if __name__ == "__main__":
    analyze_positive_dishes()