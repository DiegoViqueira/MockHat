import { User } from "./user.model";


export interface ListUsers {
    users: User[];
    total: number;
}

