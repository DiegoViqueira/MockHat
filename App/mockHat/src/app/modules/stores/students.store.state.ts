import { Student } from "../models/student.model";


export type StudentStoreQueryParams = {
  query: string;
  limit: number;
  offset: number;
};

type StudentsStoreState = {
  students: Student[];
  isLoading: boolean;
  query: StudentStoreQueryParams;
};

export const StudentsInitialState: StudentsStoreState = {
  students: [],
  isLoading: false,
  query: { query: '', limit: 1000, offset: 0 },
};
