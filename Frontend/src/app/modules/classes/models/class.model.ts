import { Institution } from "../../shared/models/institutions.enum";
import { Student } from "../../students/models/student.model";
import { Level } from "../../users/models/user-level.enum";
import { User } from "../../users/models/user.model";

export interface Class {
    _id: string;
    account_id: string;
    name: string;
    description?: string;
    institution: Institution;
    level: Level;
    teachers: User[];
    students: Student[];
    is_active: boolean;
    createdAt: Date;
    updatedAt: Date;
}

