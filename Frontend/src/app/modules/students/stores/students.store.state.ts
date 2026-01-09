import { Student } from '../models/student.model';

export type StudentStoreQueryParams = {
  query: string;
  limit: number;
  offset: number;
};

type StudentsStoreState = {
  students: Student[];
  total: number;
  isLoading: boolean;
  query: StudentStoreQueryParams;
};

export const StudentsInitialState: StudentsStoreState = {
  students: [],
  total: 0,
  isLoading: false,
  query: { query: '', limit: 1000, offset: 0 },
};
