import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
} from "typeorm";

@Entity("borrowed_books")
export class BorrowedBook {
  @PrimaryGeneratedColumn()
  id!: number;

  @Column()
  username!: string;

  @Column()
  title!: string;

  @Column()
  author!: string;

  @Column()
  genre!: string;

  @CreateDateColumn()
  borrowed_at!: Date;
}
