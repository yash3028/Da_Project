import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Library Management System", layout="wide")

BASE_URL = "http://localhost:5000/api"  # confirm this with your backend teammate

# ------------------ SESSION STATE ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


st.title("📚 Library Management System")

# ------------------ LOGIN ------------------
if not st.session_state.logged_in:
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
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
                st.session_state.user_id = data["user_id"]
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")

        except requests.exceptions.RequestException:
            st.error("Backend not reachable")


# ------------------ MAIN APP ------------------
if st.session_state.logged_in:
    st.sidebar.title("📖 Menu")

    menu = st.sidebar.radio(
        "Navigation",
        ["Genres", "Best Selling Books", "Logout"]
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

        if st.button("Proceed to Borrow"):
            st.session_state.selected_book = selected_book
            st.info("Now go to 'Borrow Book' from the sidebar")

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
        st.header("📕 Borrow a Book")
        books = pd.read_csv("data/books.csv")

        if "selected_book" in st.session_state:
            default_book = st.session_state.selected_book
        else:
            default_book = books["title"].iloc[0]

        book_title = st.selectbox(
            "Select Book",
            books["title"],
            index=list(books["title"]).index(default_book)
        )

        book = books[books["title"] == book_title].iloc[0]

        if book["is_available"] == "Yes":
            days = st.slider("Borrow Period (Days)", 7, 30)
            st.write("Deposit Amount: €10")

            if st.button("Confirm Borrow"):
                st.success("✅ Book borrowed successfully")
        else:
            st.warning("❌ Book not available")

    # ---------- LOGOUT ----------
    elif menu == "Logout":
        st.session_state.logged_in = False
        st.rerun()
