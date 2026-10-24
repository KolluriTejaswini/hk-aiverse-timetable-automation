import sqlite3
def make_db():
    db = sqlite3.connect(":memory:")
    db.executescript("""
    CREATE TABLE departments(dept_id INTEGER PRIMARY KEY, dept_name TEXT);
    CREATE TABLE students(student_id INTEGER PRIMARY KEY, dept_id INTEGER, year INTEGER);
    CREATE TABLE enrollments(student_id INTEGER, course TEXT, marks REAL);
    INSERT INTO departments VALUES (1,'AI'),(2,'CSE'),(3,'ECE'),(4,'Civil');
    INSERT INTO students VALUES (1,1,3),(2,1,3),(3,1,3),(4,1,3),(5,2,3),(6,2,3),(7,2,3),(8,3,3),(9,3,3),(10,4,3),(11,2,3),(12,1,3);
    INSERT INTO enrollments VALUES
      (1,'DBMS',78),(2,'DBMS',66),(3,'DBMS',90),(4,'OS',70),(12,'DBMS',55),
      (5,'DBMS',81),(6,'DBMS',72),(7,'DBMS',64),(11,'DBMS',88),(5,'OS',60),
      (8,'DBMS',91),(9,'DBMS',85),(10,'DBMS',40),(10,'DBMS',60);
    """)
    return db
