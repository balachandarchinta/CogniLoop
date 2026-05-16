"""
Database migration script to add new columns for enhanced features
"""
import sqlite3

def migrate_database():
    """Add new columns and tables for enhanced features"""
    conn = sqlite3.connect('learning_platform.db')
    c = conn.cursor()
    
    print("Starting database migration...")
    
    # Add video_url and duration_minutes to content table
    try:
        c.execute("ALTER TABLE content ADD COLUMN video_url TEXT")
        print("[OK] Added video_url column to content table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("[SKIP] video_url column already exists")
        else:
            print(f"[ERROR] {e}")
    
    try:
        c.execute("ALTER TABLE content ADD COLUMN duration_minutes INTEGER")
        print("[OK] Added duration_minutes column to content table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("[SKIP] duration_minutes column already exists")
        else:
            print(f"[ERROR] {e}")
    
    # Create quizzes table
    try:
        c.execute('''CREATE TABLE IF NOT EXISTS quizzes
                     (id TEXT PRIMARY KEY,
                      content_id TEXT,
                      title TEXT NOT NULL,
                      description TEXT,
                      questions TEXT,
                      passing_score INTEGER DEFAULT 70,
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                      FOREIGN KEY (content_id) REFERENCES content(id))''')
        print("[OK] Created quizzes table")
    except Exception as e:
        print(f"[ERROR] Creating quizzes table: {e}")
    
    # Create quiz_attempts table
    try:
        c.execute('''CREATE TABLE IF NOT EXISTS quiz_attempts
                     (id TEXT PRIMARY KEY,
                      user_id TEXT,
                      quiz_id TEXT,
                      score INTEGER,
                      answers TEXT,
                      passed BOOLEAN,
                      completed_at TIMESTAMP,
                      FOREIGN KEY (user_id) REFERENCES users(id),
                      FOREIGN KEY (quiz_id) REFERENCES quizzes(id))''')
        print("[OK] Created quiz_attempts table")
    except Exception as e:
        print(f"[ERROR] Creating quiz_attempts table: {e}")
    
    # Create assignments table
    try:
        c.execute('''CREATE TABLE IF NOT EXISTS assignments
                     (id TEXT PRIMARY KEY,
                      content_id TEXT,
                      title TEXT NOT NULL,
                      description TEXT,
                      instructions TEXT,
                      due_date TIMESTAMP,
                      max_score INTEGER DEFAULT 100,
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                      FOREIGN KEY (content_id) REFERENCES content(id))''')
        print("[OK] Created assignments table")
    except Exception as e:
        print(f"[ERROR] Creating assignments table: {e}")
    
    # Create assignment_submissions table
    try:
        c.execute('''CREATE TABLE IF NOT EXISTS assignment_submissions
                     (id TEXT PRIMARY KEY,
                      user_id TEXT,
                      assignment_id TEXT,
                      submission_text TEXT,
                      score INTEGER,
                      feedback TEXT,
                      submitted_at TIMESTAMP,
                      graded_at TIMESTAMP,
                      FOREIGN KEY (user_id) REFERENCES users(id),
                      FOREIGN KEY (assignment_id) REFERENCES assignments(id))''')
        print("[OK] Created assignment_submissions table")
    except Exception as e:
        print(f"[ERROR] Creating assignment_submissions table: {e}")
    
    conn.commit()
    conn.close()
    
    print("\nMigration completed successfully!")

if __name__ == "__main__":
    migrate_database()

# Made with Bob
