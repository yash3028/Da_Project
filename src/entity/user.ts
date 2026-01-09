import { Entity, PrimaryGeneratedColumn, Column } from "typeorm";

@Entity()
export class users {
  @PrimaryGeneratedColumn()
  id!: number;

  @Column({ unique: true })
  username!: string;

  @Column()
  password!: string;

  @Column({ nullable: true })
  token!: string;

  @Column()
  email!: string;
}
