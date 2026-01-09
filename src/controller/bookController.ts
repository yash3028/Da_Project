import { Router, Request, Response } from "express";
import { readBooks, borrowBook, getMyBooks } from "../services/bookServices";

const router = Router();

router.get("/", async (req: Request, res: Response) => {
  const books = await readBooks();
  res.json(books);
});

router.post("/borrow", async (req: Request, res: Response) => {
  try {
    const { title, username } = req.body;
    await borrowBook(title, username);
    res.json({ message: "Book borrowed successfully" });
  } catch (error: any) {
    res.status(400).json({ message: error.message });
  }
});

router.get("/my-books/:username", async (req: Request, res: Response) => {
  const { username } = req.params;

  if (!username) {
    return res.status(400).json({ message: "Username is required" });
  }

  const books = await getMyBooks(username);
  res.json(books);
});

export = router;
