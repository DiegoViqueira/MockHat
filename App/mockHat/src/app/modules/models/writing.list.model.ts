import { Writing } from "./writing.model";


export interface WritingListResult {
    writings: Writing[];
    total?: number;
}