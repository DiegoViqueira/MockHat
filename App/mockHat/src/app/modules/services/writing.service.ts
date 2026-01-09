import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Writing } from '../models/writing.model';
import { WritingTask } from '../models/writing.task.model';
import { Level } from '../models/user-level.enum';
import { HttpService } from 'src/app/@core/services/http.service';
import { WritingListResult } from '../models/writing.list.model';
import { RatingUpdateRequest } from '../models/rating-update-request.model';

@Injectable({
  providedIn: 'root',
})
export class WritingService {
  constructor(private readonly api: HttpService) { }

  evaluate(
    student_id: string,
    level: Level,
    question: string,
    task: WritingTask,
    imageBlob: Blob
  ): Observable<Writing> {
    const formData = new FormData();
    formData.append('student_id', student_id);
    formData.append('level', level);
    formData.append('question', question);
    formData.append('task', task);
    formData.append('file', imageBlob, 'image.jpg');

    return this.api.post(`writing`, formData).pipe(
      map((response) => {
        return response;
      })
    );
  }

  search(limit: number = 10, offset: number = 0): Observable<WritingListResult> {
    return this.api.get(`writing?limit=${limit}&offset=${offset}`).pipe(
      map((response) => {
        return response;
      })
    );
  }

  rate(writing: Writing, rating: RatingUpdateRequest): Observable<void> {
    return this.api.patch(`writing/rate`, writing._id, rating).pipe(
      map((response) => {
        return response;
      })
    );
  }

  translateTask(audioBlob: Blob, task: WritingTask): Observable<string> {
    const formData = new FormData();
    formData.append('file', audioBlob, 'image.jpg');
    formData.append('task', task);
    return this.api.post(`writing/translate/assessment`, formData).pipe(
      map((response) => {
        return response;
      })
    );
  }

  translateAnswer(
    writing_id: string,
    student_id: string,
    audioBlob: Blob,
    task: WritingTask
  ): Observable<Writing> {
    const formData = new FormData();
    formData.append('file', audioBlob, 'image.jpg');
    formData.append('task', task);
    formData.append('writing_id', writing_id);
    formData.append('student_id', student_id);

    return this.api.post(`writing/translate/answer`, formData).pipe(
      map((response) => {
        return response;
      })
    );
  }
}
