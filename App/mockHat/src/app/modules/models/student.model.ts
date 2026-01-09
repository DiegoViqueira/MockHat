import { Level } from "./user-level.enum";

export interface Student {
  id?: string;
  name?: string;
  last_name?: string;
  teacher_id?: string;
  level?: Level;
  created_at: Date;
  updated_at: Date;
}
