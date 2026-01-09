import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Library Management System", layout="wide")

BASE_URL = "http://localhost:3002/api/auth"  
BOOKS_URL = "http://localhost:3002/api/books"
# ------------------ SESSION STATE ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
# st.title("📚 Library Management System")
if "menu" not in st.session_state:
    st.session_state.menu = "Genres"

if "next_menu" not in st.session_state:
    st.session_state.next_menu = None

# ------------------ LOGIN ------------------
if not st.session_state.logged_in:
    st.title("📚 Library Management System")

    signin_tab, signup_tab = st.tabs(["Sign In", "Sign Up"])

    # ---------------- SIGN IN ----------------
    with signin_tab:
        st.subheader("Sign In")

        username = st.text_input("Username", key="signin_username")
        password = st.text_input("Password", type="password", key="signin_password")
        
        if st.button("Sign In"):
            try:
                response = requests.post(
                    f"{BASE_URL}/login",
                    json={
                        "username": username,
                        "password": password
                    }
                )

                if response.status_code == 200:
                    data = response.json()
                    st.session_state.logged_in = True
                    st.session_state.username = username   
                    st.session_state.menu = "Genres"

                    st.success("Login successful")
                    st.rerun()
                else:
                    st.error("Invalid credentials")

            except requests.exceptions.RequestException:
                st.error("Backend not reachable")

    # ---------------- SIGN UP ----------------
    with signup_tab:
        st.subheader("Sign Up")

        new_username = st.text_input("Username", key="signup_username")
        new_email = st.text_input("Email", key="signup_email")
        new_password = st.text_input("Password", type="password", key="signup_password")
        confirm_password = st.text_input(
            "Confirm Password", type="password", key="signup_confirm"
        )
        payload = {"username": new_username, "email": new_email, "password": new_password}
        if st.button("Create Account"):
            if new_password != confirm_password:
                st.error("Passwords do not match")
            elif not new_username or not new_email or not new_password:
                st.error("All fields are required")
            else:
                try:
                    response = requests.post(
                        f"{BASE_URL}/save-user",
                        json=payload
                    )

                    if response.status_code == 201:
                        st.success("Account created successfully. Please sign in.")
                    else:
                        try:
                            st.error(response.json().get("message", "Signup failed"))
                        except Exception:
                            st.error(f"Signup failed (status {response.status_code})")
                except Exception as e:
                    st.error(f"Request failed: {e}")

# ------------------ MAIN APP ------------------
if st.session_state.logged_in:
    st.sidebar.title("📖 Menu")

    menu_options = [
    "Genres",
    "Best Selling Books",
    "Borrow Book",
    "My Borrowed Books",
    "Top Authors",
    "Education",
    "Logout"
]
    if st.session_state.next_menu is not None:
        st.session_state.menu = st.session_state.next_menu
        st.session_state.next_menu = None
    menu = st.sidebar.radio(
    "Navigation",
    menu_options,
    index=menu_options.index(st.session_state.menu),
    key="menu"   
)
    
    # ---------- GENRES ----------
    if menu == "Genres":
        st.header("📚 Book Genres")

        genres = pd.read_csv("data/genres.csv")
        books = pd.read_csv("data/books.csv")

        selected_genre = st.selectbox(
                "Select a Genre",
                genres["genre_name"]
            )

        filtered_books = books[books["genre"] == selected_genre]

        st.subheader(f"Books in {selected_genre}")
        st.dataframe(
                filtered_books[["title", "author", "is_available"]],
                use_container_width=True
            )

        selected_book = st.selectbox(
                "Select a book to borrow",
                filtered_books["title"]
            )
        book_status = filtered_books[
            filtered_books["title"] == selected_book
        ]["is_available"].values[0]

        if book_status != "Yes":
            st.warning("❌ This book is currently not available")
        else:
            if st.button("Proceed to Borrow"):
                st.session_state.selected_book = selected_book
                st.session_state.next_menu = "Borrow Book"
                st.rerun()
    # ---------- BEST SELLING BOOKS ----------
    elif menu == "Best Selling Books":
            st.header("🔥 Best Selling Books")
            best = pd.read_csv("data/best_selling_books.csv")
            st.dataframe(best, use_container_width=True)

    # ---------- TOP AUTHORS ----------
    elif menu == "Top Authors":
            st.header("✍️ Top Authors")
            authors = pd.read_csv("data/authors.csv")

            top_n = st.selectbox("Select Top Authors", [3, 5])
            st.dataframe(
                authors.sort_values("borrow_count", ascending=False).head(top_n),
                use_container_width=True
            )

    # ---------- EDUCATION ----------
    elif menu == "Education":
            st.header("🎓 Academic Resources")
            courses = pd.read_csv("data/courses.csv")
            subjects = pd.read_csv("data/subjects_books.csv")

            course = st.selectbox("Select Course", courses["course_name"])
            duration = courses[courses["course_name"] == course]["duration"].values[0]

            st.info(f"Course Duration: {duration}")
            st.dataframe(
                subjects[subjects["course_name"] == course],
                use_container_width=True
            )
    # ---------- BORROW BOOK ----------
    elif menu == "Borrow Book":
        st.header("📕 Borrow Book")

        if "selected_book" not in st.session_state:
            st.warning("Please select a book from Genres first.")
        else:
            st.write(f"Selected Book: {st.session_state.selected_book}")

            if st.button("Confirm Borrow"):
                try:
                    response = requests.post(
                        f"{BOOKS_URL}/borrow",
                        json={
                            "title": st.session_state.selected_book,
                            "username": st.session_state.username
                        }
                    )

                    if response.status_code == 200:
                        st.success("Book borrowed successfully")
                        del st.session_state.selected_book
                    else:
                        st.error(response.json().get("message", "Borrow failed"))
                except Exception as e:
                    st.error(f"Backend error: {e}")
    # ---------- BORROW BOOK ----------
    elif menu == "My Borrowed Books":
            st.header("📘 My Borrowed Books")

            try:
                response = requests.get(
                    f"{BOOKS_URL}/my-books/{st.session_state.username}"
                )

                if response.status_code == 200:
                    borrowed_books = pd.DataFrame(response.json())

                    if borrowed_books.empty:
                        st.info("You have not borrowed any books.")
                    else:
                        st.dataframe(
                            borrowed_books[
                                ["username","title", "author", "genre", "borrowed_at"]
                            ],
                            use_container_width=True,
                        )
                else:
                    st.error("Failed to fetch borrowed books")
            except Exception as e:
                st.error(f"Backend error: {e}")
    # ---------- LOGOUT ----------
    elif menu == "Logout":
            st.session_state.clear()
            st.rerun()
