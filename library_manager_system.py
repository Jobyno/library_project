 # Campus Library Manager - A Book Rental and Inventory System
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
import json
import os

# Global Data Storage
books: Dict[str, Dict] = {
    "B001": {
        "title": "Python Programming",
        "author": "John Smith",
        "genre": "Technology",
        "total_copies": 5,
        "available_copies": 3,
        "checkout_count": 15,
        "publication_year": 2022
    },
    "B002": {
        "title": "Data Structures",
        "author": "Jane Doe",
        "genre": "Computer Science",
        "total_copies": 3,
        "available_copies": 1,
        "checkout_count": 25,
        "publication_year": 2021
    },
    "B003": {
        "title": "Web Development",
        "author": "Bob Wilson",
        "genre": "Technology",
        "total_copies": 4,
        "available_copies": 4,
        "checkout_count": 8,
        "publication_year": 2023
    }
}

# Transaction records: {transaction_id: {book_id, student_id, checkout_date, due_date, return_date, fine}}
transactions: Dict[str, Dict] = {
    "T001": {
        "book_id": "B001",
        "student_id": "S001",
        "student_name": "Alice Johnson",
        "checkout_date": "2024-01-15",
        "due_date": "2024-01-29",
        "return_date": None,
        "fine": 0.0,
        "status": "borrowed"
    },
    "T002": {
        "book_id": "B002",
        "student_id": "S002",
        "student_name": "David Brown",
        "checkout_date": "2024-01-10",
        "due_date": "2024-01-24",
        "return_date": "2024-01-22",
        "fine": 0.0,
        "status": "returned"
    }
}

# Configuration
LOAN_PERIOD_DAYS = 14
FINE_PER_DAY = 2.0
MAX_BOOKS_PER_STUDENT = 3

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_current_date():
    """Get current date as string"""
    return datetime.now().strftime("%Y-%m-%d")

def parse_date(date_str):
    """Parse date string to datetime object"""
    return datetime.strptime(date_str, "%Y-%m-%d")

def calculate_days_difference(date1_str, date2_str):
    """Calculate difference in days between two dates"""
    date1 = parse_date(date1_str)
    date2 = parse_date(date2_str)
    return (date2 - date1).days

def generate_transaction_id():
    """Generate next transaction ID"""
    if not transactions:
        return "T001"
    
    max_id = max([int(tid[1:]) for tid in transactions.keys()])
    return f"T{max_id + 1:03d}"

def book_exists(book_id):
    """Check if book exists"""
    return book_id in books

def get_student_active_loans(student_id):
    """Get number of active loans for a student"""
    count = 0
    for trans in transactions.values():
        if trans["student_id"] == student_id and trans["status"] == "borrowed":
            count += 1
    return count

# =============================================================================
# A. INVENTORY MANAGEMENT MODULE
# =============================================================================

def add_book():
    """Add a new book to the inventory"""
    print("\n=== ADD NEW BOOK ===")
    
    book_id = input("Enter Book ID (e.g., B004): ").strip().upper()
    
    if book_exists(book_id):
        print(f"Book with ID {book_id} already exists!")
        return
    
    title = input("Enter book title: ").strip()
    author = input("Enter author name: ").strip()
    genre = input("Enter genre: ").strip()
    
    try:
        total_copies = int(input("Enter total copies: ").strip())
        pub_year = int(input("Enter publication year: ").strip())
        
        if total_copies <= 0:
            print("Total copies must be greater than 0!")
            return
            
    except ValueError:
        print("Please enter valid numbers for copies and year!")
        return
    
    books[book_id] = {
        "title": title,
        "author": author,
        "genre": genre,
        "total_copies": total_copies,
        "available_copies": total_copies,
        "checkout_count": 0,
        "publication_year": pub_year
    }
    
    print(f"Book '{title}' added successfully with ID: {book_id}")

def update_book():
    """Update existing book information"""
    print("\n=== UPDATE BOOK ===")
    
    book_id = input("Enter Book ID to update: ").strip().upper()
    
    if not book_exists(book_id):
        print(f"Book with ID {book_id} not found!")
        return
    
    book = books[book_id]
    print(f"\nCurrent book details:")
    print(f"Title: {book['title']}")
    print(f"Author: {book['author']}")
    print(f"Genre: {book['genre']}")
    print(f"Total Copies: {book['total_copies']}")
    print(f"Publication Year: {book['publication_year']}")
    
    print("\nEnter new values (press Enter to keep current value):")
    
    new_title = input(f"New title [{book['title']}]: ").strip()
    new_author = input(f"New author [{book['author']}]: ").strip()
    new_genre = input(f"New genre [{book['genre']}]: ").strip()
    new_copies = input(f"New total copies [{book['total_copies']}]: ").strip()
    new_year = input(f"New publication year [{book['publication_year']}]: ").strip()
    
    # Update only if new values provided
    if new_title:
        book['title'] = new_title
    if new_author:
        book['author'] = new_author
    if new_genre:
        book['genre'] = new_genre
    if new_copies:
        try:
            copies = int(new_copies)
            if copies >= book['total_copies'] - book['available_copies']:
                book['total_copies'] = copies
            else:
                print("Total copies cannot be less than currently borrowed books!")
                return
        except ValueError:
            print("Invalid number for copies!")
            return
    if new_year:
        try:
            book['publication_year'] = int(new_year)
        except ValueError:
            print("Invalid year!")
            return
    
    print("Book updated successfully!")

def display_all_books():
    """Display all books in the inventory"""
    print("\n" + "="*100)
    print("                                    LIBRARY INVENTORY")
    print("="*100)
    print(f"{'ID':<6} {'Title':<25} {'Author':<20} {'Genre':<15} {'Total':<6} {'Available':<10} {'Borrowed':<8}")
    print("-"*100)
    
    if not books:
        print("No books in inventory!")
        return
    
    for book_id, book in books.items():
        borrowed = book['total_copies'] - book['available_copies']
        print(f"{book_id:<6} {book['title'][:24]:<25} {book['author'][:19]:<20} "
              f"{book['genre'][:14]:<15} {book['total_copies']:<6} {book['available_copies']:<10} {borrowed:<8}")
    
    print("-"*100)
    print(f"Total Books: {len(books)} | Total Copies: {sum(b['total_copies'] for b in books.values())}")

def search_books():
    """Search books by title, author, or genre"""
    print("\n=== SEARCH BOOKS ===")
    print("1. Search by Title")
    print("2. Search by Author")
    print("3. Search by Genre")
    
    try:
        choice = int(input("Choose search type: ").strip())
    except ValueError:
        print("Invalid choice!")
        return
    
    if choice not in [1, 2, 3]:
        print("Invalid choice!")
        return
    
    search_term = input("Enter search term: ").strip().lower()
    
    if not search_term:
        print("Search term cannot be empty!")
        return
    
    found_books = []
    
    for book_id, book in books.items():
        if choice == 1 and search_term in book['title'].lower():
            found_books.append((book_id, book))
        elif choice == 2 and search_term in book['author'].lower():
            found_books.append((book_id, book))
        elif choice == 3 and search_term in book['genre'].lower():
            found_books.append((book_id, book))
    
    if not found_books:
        print("No books found matching your search!")
        return
    
    print(f"\nFound {len(found_books)} book(s):")
    print("-"*80)
    print(f"{'ID':<6} {'Title':<25} {'Author':<20} {'Available':<10}")
    print("-"*80)
    
    for book_id, book in found_books:
        print(f"{book_id:<6} {book['title'][:24]:<25} {book['author'][:19]:<20} {book['available_copies']:<10}")

# =============================================================================
# B. ORDER PROCESSING MODULE
# =============================================================================

def checkout_book():
    """Process book checkout"""
    print("\n=== CHECKOUT BOOK ===")
    
    student_id = input("Enter Student ID: ").strip().upper()
    student_name = input("Enter Student Name: ").strip()
    book_id = input("Enter Book ID: ").strip().upper()
    
    if not student_id or not student_name or not book_id:
        print("All fields are required!")
        return
    
    # Check if book exists
    if not book_exists(book_id):
        print(f"Book with ID {book_id} not found!")
        return
    
    # Check if book is available
    if books[book_id]['available_copies'] <= 0:
        print(f"Book '{books[book_id]['title']}' is not available for checkout!")
        return
    
    # Check student's current loans
    active_loans = get_student_active_loans(student_id)
    if active_loans >= MAX_BOOKS_PER_STUDENT:
        print(f"Student has reached maximum loan limit of {MAX_BOOKS_PER_STUDENT} books!")
        return
    
    # Process checkout
    transaction_id = generate_transaction_id()
    checkout_date = get_current_date()
    due_date = (datetime.now() + timedelta(days=LOAN_PERIOD_DAYS)).strftime("%Y-%m-%d")
    
    transactions[transaction_id] = {
        "book_id": book_id,
        "student_id": student_id,
        "student_name": student_name,
        "checkout_date": checkout_date,
        "due_date": due_date,
        "return_date": None,
        "fine": 0.0,
        "status": "borrowed"
    }
    
    # Update book availability
    books[book_id]['available_copies'] -= 1
    books[book_id]['checkout_count'] += 1
    
    print(f"\nCheckout successful!")
    print(f"Transaction ID: {transaction_id}")
    print(f"Book: {books[book_id]['title']}")
    print(f"Due Date: {due_date}")
    print(f"Student: {student_name} ({student_id})")

def return_book():
    """Process book return"""
    print("\n=== RETURN BOOK ===")
    
    transaction_id = input("Enter Transaction ID: ").strip().upper()
    
    if transaction_id not in transactions:
        print("Transaction ID not found!")
        return
    
    transaction = transactions[transaction_id]
    
    if transaction['status'] == 'returned':
        print("This book has already been returned!")
        return
    
    book_id = transaction['book_id']
    return_date = get_current_date()
    
    # Calculate fine if overdue
    fine = 0.0
    days_overdue = calculate_days_difference(transaction['due_date'], return_date)
    
    if days_overdue > 0:
        fine = days_overdue * FINE_PER_DAY
        print(f"Book is {days_overdue} days overdue!")
        print(f"Fine amount: ${fine:.2f}")
    
    # Update transaction
    transaction['return_date'] = return_date
    transaction['fine'] = fine
    transaction['status'] = 'returned'
    
    # Update book availability
    books[book_id]['available_copies'] += 1
    
    print(f"\nReturn processed successfully!")
    print(f"Book: {books[book_id]['title']}")
    print(f"Student: {transaction['student_name']}")
    print(f"Return Date: {return_date}")
    if fine > 0:
        print(f"Fine: ${fine:.2f}")

def view_overdue_books():
    """Display all overdue books"""
    print("\n=== OVERDUE BOOKS ===")
    current_date = get_current_date()
    
    overdue_transactions = []
    
    for trans_id, trans in transactions.items():
        if trans['status'] == 'borrowed':
            days_overdue = calculate_days_difference(trans['due_date'], current_date)
            if days_overdue > 0:
                fine = days_overdue * FINE_PER_DAY
                overdue_transactions.append((trans_id, trans, days_overdue, fine))
    
    if not overdue_transactions:
        print("No overdue books!")
        return
    
    print(f"{'Trans ID':<8} {'Book Title':<25} {'Student':<20} {'Days Late':<10} {'Fine':<8}")
    print("-"*80)
    
    total_fines = 0.0
    for trans_id, trans, days_late, fine in overdue_transactions:
        book_title = books[trans['book_id']]['title'][:24]
        student_name = trans['student_name'][:19]
        print(f"{trans_id:<8} {book_title:<25} {student_name:<20} {days_late:<10} ${fine:<7.2f}")
        total_fines += fine
    
    print("-"*80)
    print(f"Total Overdue Books: {len(overdue_transactions)} | Total Fines: ${total_fines:.2f}")

# =============================================================================
# C. REPORTING MODULE
# =============================================================================

def inventory_report():
    """Generate real-time inventory report"""
    print("\n" + "="*80)
    print("                           INVENTORY REPORT")
    print("="*80)
    
    total_books = len(books)
    total_copies = sum(book['total_copies'] for book in books.values())
    total_available = sum(book['available_copies'] for book in books.values())
    total_borrowed = total_copies - total_available
    
    print(f"Report Date: {get_current_date()}")
    print(f"Total Book Titles: {total_books}")
    print(f"Total Copies: {total_copies}")
    print(f"Available Copies: {total_available}")
    print(f"Borrowed Copies: {total_borrowed}")
    print(f"Utilization Rate: {(total_borrowed/total_copies)*100:.1f}%" if total_copies > 0 else "N/A")
    
    print("\n" + "="*80)
    print("BOOKS BY AVAILABILITY STATUS")
    print("="*80)
    
    available_books = [(bid, book) for bid, book in books.items() if book['available_copies'] > 0]
    unavailable_books = [(bid, book) for bid, book in books.items() if book['available_copies'] == 0]
    
    print(f"\nAvailable Books ({len(available_books)}):")
    print("-"*50)
    for book_id, book in available_books[:10]:  # Show top 10
        print(f"{book_id}: {book['title']} - {book['available_copies']} copies")
    
    if unavailable_books:
        print(f"\nUnavailable Books ({len(unavailable_books)}):")
        print("-"*50)
        for book_id, book in unavailable_books:
            print(f"{book_id}: {book['title']}")

def popular_books_report():
    """Generate report of most popular books"""
    print("\n=== POPULAR BOOKS REPORT ===")
    
    # Sort books by checkout count
    popular_books = sorted(books.items(), key=lambda x: x[1]['checkout_count'], reverse=True)
    
    print(f"{'Rank':<5} {'Book ID':<8} {'Title':<30} {'Checkouts':<10} {'Genre':<15}")
    print("-"*75)
    
    for i, (book_id, book) in enumerate(popular_books[:10], 1):
        print(f"{i:<5} {book_id:<8} {book['title'][:29]:<30} {book['checkout_count']:<10} {book['genre'][:14]:<15}")
    
    # High demand alert
    high_demand_books = [book for book in books.values() if book['checkout_count'] > 20]
    if high_demand_books:
        print(f"\n🚨 HIGH DEMAND ALERT: {len(high_demand_books)} books have >20 checkouts!")
        print("Consider adding more copies for these titles.")

def transaction_summary():
    """Generate transaction summary report"""
    print("\n=== TRANSACTION SUMMARY ===")
    
    current_date = get_current_date()
    
    # Active loans
    active_loans = [t for t in transactions.values() if t['status'] == 'borrowed']
    
    # Completed returns
    completed_returns = [t for t in transactions.values() if t['status'] == 'returned']
    
    # Calculate total fines
    total_fines = sum(t['fine'] for t in transactions.values())
    pending_fines = 0.0
    
    # Calculate pending fines for overdue books
    for trans in active_loans:
        days_overdue = calculate_days_difference(trans['due_date'], current_date)
        if days_overdue > 0:
            pending_fines += days_overdue * FINE_PER_DAY
    
    print(f"Report Date: {current_date}")
    print(f"Total Transactions: {len(transactions)}")
    print(f"Active Loans: {len(active_loans)}")
    print(f"Completed Returns: {len(completed_returns)}")
    print(f"Total Fines Collected: ${total_fines:.2f}")
    print(f"Pending Fines (Overdue): ${pending_fines:.2f}")
    
    # Recent transactions (last 5)
    recent_trans = list(transactions.items())[-5:]
    if recent_trans:
        print(f"\nRecent Transactions:")
        print("-"*60)
        for trans_id, trans in recent_trans:
            book_title = books[trans['book_id']]['title'][:20]
            status = trans['status']
            print(f"{trans_id}: {book_title} - {trans['student_name']} ({status})")

def student_activity_report():
    """Generate student activity report"""
    print("\n=== STUDENT ACTIVITY REPORT ===")
    
    # Group transactions by student
    student_stats = {}
    
    for trans in transactions.values():
        student_id = trans['student_id']
        if student_id not in student_stats:
            student_stats[student_id] = {
                'name': trans['student_name'],
                'total_loans': 0,
                'active_loans': 0,
                'total_fines': 0.0
            }
        
        student_stats[student_id]['total_loans'] += 1
        if trans['status'] == 'borrowed':
            student_stats[student_id]['active_loans'] += 1
        student_stats[student_id]['total_fines'] += trans['fine']
    
    print(f"{'Student ID':<12} {'Name':<20} {'Total Loans':<12} {'Active':<8} {'Fines':<8}")
    print("-"*65)
    
    for student_id, stats in student_stats.items():
        print(f"{student_id:<12} {stats['name'][:19]:<20} {stats['total_loans']:<12} "
              f"{stats['active_loans']:<8} ${stats['total_fines']:<7.2f}")

# =============================================================================
# MAIN MENU SYSTEM
# =============================================================================

def inventory_menu():
    """Inventory management submenu"""
    while True:
        print("\n" + "="*50)
        print("         INVENTORY MANAGEMENT")
        print("="*50)
        print("1. Add New Book")
        print("2. Update Book Information")
        print("3. Display All Books")
        print("4. Search Books")
        print("0. Back to Main Menu")
        
        try:
            choice = int(input("\nSelect option: ").strip())
        except ValueError:
            print("Please enter a valid number!")
            continue
        
        if choice == 1:
            add_book()
        elif choice == 2:
            update_book()
        elif choice == 3:
            display_all_books()
        elif choice == 4:
            search_books()
        elif choice == 0:
            break
        else:
            print("Invalid option! Please try again.")

def transaction_menu():
    """Transaction processing submenu"""
    while True:
        print("\n" + "="*50)
        print("         TRANSACTION PROCESSING")
        print("="*50)
        print("1. Checkout Book")
        print("2. Return Book")
        print("3. View Overdue Books")
        print("0. Back to Main Menu")
        
        try:
            choice = int(input("\nSelect option: ").strip())
        except ValueError:
            print("Please enter a valid number!")
            continue
        
        if choice == 1:
            checkout_book()
        elif choice == 2:
            return_book()
        elif choice == 3:
            view_overdue_books()
        elif choice == 0:
            break
        else:
            print("Invalid option! Please try again.")

def reports_menu():
    """Reports submenu"""
    while True:
        print("\n" + "="*50)
        print("              REPORTS")
        print("="*50)
        print("1. Inventory Report")
        print("2. Popular Books Report")
        print("3. Transaction Summary")
        print("4. Student Activity Report")
        print("0. Back to Main Menu")
        
        choice_input = input("\nSelect option: ").strip()
        
        if not choice_input.isdigit() or len(choice_input) != 1:
            print("Please enter a valid single digit (0-4)!")
            input("Press Enter to continue...")
            continue
        
        choice = int(choice_input)
        
        if choice == 1:
            inventory_report()
        elif choice == 2:
            popular_books_report()
        elif choice == 3:
            transaction_summary()
        elif choice == 4:
            student_activity_report()
        elif choice == 0:
            break
        else:
            print("Invalid option! Please enter a number between 0-4.")
            input("Press Enter to continue...")

def main_menu():
    """Main application menu"""
    print("\n" + "="*60)
    print("    WELCOME TO CAMPUS LIBRARY MANAGER")
    print("="*60)
    print("         Streamlining Library Operations")
    print("="*60)
    
    while True:
        print(f"\nCurrent Date: {get_current_date()}")
        print("\n" + "="*50)
        print("              MAIN MENU")
        print("="*50)
        print("1. Inventory Management")
        print("2. Transaction Processing")
        print("3. Reports & Analytics")
        print("4. System Status")
        print("0. Exit System")
        
        try:
            choice = int(input("\nSelect option: ").strip())
        except ValueError:
            print("Please enter a valid number!")
            continue
        
        if choice == 1:
            inventory_menu()
        elif choice == 2:
            transaction_menu()
        elif choice == 3:
            reports_menu()
        elif choice == 4:
            display_system_status()
        elif choice == 0:
            print("\nThank you for using Campus Library Manager!")
            print("System shutting down...")
            break
        else:
            print("Invalid option! Please try again.")

def display_system_status():
    """Display quick system status"""
    print("\n" + "="*60)
    print("                    SYSTEM STATUS")
    print("="*60)
    
    total_books = len(books)
    total_copies = sum(book['total_copies'] for book in books.values())
    available_copies = sum(book['available_copies'] for book in books.values())
    active_loans = len([t for t in transactions.values() if t['status'] == 'borrowed'])
    
    # Calculate overdue books
    current_date = get_current_date()
    overdue_count = 0
    for trans in transactions.values():
        if trans['status'] == 'borrowed':
            if calculate_days_difference(trans['due_date'], current_date) > 0:
                overdue_count += 1
    
    print(f"📚 Total Book Titles: {total_books}")
    print(f"📖 Total Copies: {total_copies}")
    print(f"✅ Available Copies: {available_copies}")
    print(f"📋 Active Loans: {active_loans}")
    print(f"⚠️  Overdue Books: {overdue_count}")
    print(f"💰 System Configuration:")
    print(f"   - Loan Period: {LOAN_PERIOD_DAYS} days")
    print(f"   - Fine Rate: ${FINE_PER_DAY}/day")
    print(f"   - Max Books per Student: {MAX_BOOKS_PER_STUDENT}")
    
    if overdue_count > 0:
        print(f"\n🚨 ACTION REQUIRED: {overdue_count} books are overdue!")

# =============================================================================
# MAIN PROGRAM EXECUTION
# =============================================================================

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nSystem interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please contact system administrator.")