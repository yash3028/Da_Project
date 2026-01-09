import fs from "fs";
import csv from "csv-parser";
import path from "path";
import { data_source } from "../config/database";
import { BorrowedBook } from "../entity/BorrowedBook";

const BOOKS_FILE = path.join(__dirname, "books.csv");

export const readBooks = (): Promise<any[]> => {
  return new Promise((resolve, reject) => {
    const books: any[] = [];

    fs.createReadStream(BOOKS_FILE)
      .pipe(csv())
      .on("data", (row) => books.push(row))
      .on("end", () => resolve(books))
      .on("error", reject);
  });
};

export const writeBooks = (books: any[]) => {
  const header = "title,author,genre,is_available,borrowed_by\n";

  const rows = books.map(
    (b) =>
      `${b.title},${b.author},${b.genre},${b.is_available},${
        b.borrowed_by || ""
      }`
  );

  fs.writeFileSync(BOOKS_FILE, header + rows.join("\n"));
};

export const borrowBook = async (title: string, username: string) => {
  const books = await readBooks();

  const book = books.find((b) => b.title === title);
  if (!book) throw new Error("Book not found");

  if (book.is_available !== "Yes") {
    throw new Error("Book not available");
  }

  book.is_available = "No";
  book.borrowed_by = username;
  writeBooks(books);

  const repo = data_source.getRepository(BorrowedBook);

  const borrowed = repo.create({
    username,
    title: book.title,
    author: book.author,
    genre: book.genre,
  });

  await repo.save(borrowed);
};

export const getMyBooks = async (username: string) => {
  const repo = data_source.getRepository(BorrowedBook);

  return await repo.find({
    where: { username },
    order: { borrowed_at: "DESC" },
  });
};
