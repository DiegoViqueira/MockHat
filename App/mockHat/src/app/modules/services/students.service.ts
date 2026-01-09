import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Student } from '../models/student.model';
import { HttpService } from 'src/app/@core/services/http.service';

@Injectable({
  providedIn: 'root',
})
export class StudentsService {
  constructor(private readonly api: HttpService) { }

  create(student: Student): Observable<Student> {
    return this.api.post(`students`, student).pipe(
      map((response) => {
        return response;
      })
    );
  }

  update(student: Student): Observable<Student> {
    if (!student.id) {
      throw new Error('Student ID is required');
    }
    return this.api.patch(`students`, student.id, student).pipe(
      map((response) => {
        return response;
      })
    );
  }

  delete(student: Student): Observable<Student> {
    if (!student.id) {
      throw new Error('Student ID is required');
    }
    return this.api.delete(`students`, student.id).pipe(
      map((response) => {
        return response;
      })
    );
  }

  search(limit: number = 10, offset: number = 0): Observable<Student[]> {
    return this.api.get(`students?limit=${limit}&offset=${offset}`).pipe(
      map((response) => {
        return response;
      })
    );
  }
}
