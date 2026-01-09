import { Injectable } from '@angular/core';
import { HttpService } from '../../../@core/services/http.service';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Student } from '../models/student.model';
import { ListStudents } from '../models/listStudents.model';

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
    return this.api.patch(`students`, student._id, student).pipe(
      map((response) => {
        return response;
      })
    );
  }

  actives(): Observable<ListStudents> {
    return this.api.get(`students/actives`).pipe(
      map((response) => {
        return response;
      })
    );
  }

  delete(student: Student): Observable<Student> {
    return this.api.delete(`students`, student._id).pipe(
      map((response) => {
        return response;
      })
    );
  }

  search(limit: number = 10, offset: number = 0): Observable<ListStudents> {
    return this.api.get(`students?limit=${limit}&offset=${offset}`).pipe(
      map((response) => {
        return response;
      })
    );
  }
}
