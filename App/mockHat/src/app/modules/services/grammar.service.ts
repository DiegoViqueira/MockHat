import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Grammar } from '../models/grammar.model';
import { GrammarListResult } from '../models/grammar.list.result.model';
import { HttpService } from 'src/app/@core/services/http.service';
import { RatingUpdateRequest } from '../models/rating-update-request.model';

@Injectable({
  providedIn: 'root',
})
export class GrammarService {
  constructor(private readonly api: HttpService) { }

  rate(grammar: Grammar, rating: RatingUpdateRequest): Observable<void> {
    return this.api.patch(`grammar/rate`, grammar._id, rating).pipe(
      map((response) => {
        return response;
      })
    );
  }

  search(limit: number = 10, offset: number = 0): Observable<GrammarListResult> {
    return this.api.get(`grammar?limit=${limit}&offset=${offset}`).pipe(
      map((response) => {
        return response;
      })
    );
  }

  check(imageBlob: Blob, grammar: Grammar): Observable<Grammar> {
    const formData = new FormData();
    if (grammar.student_id) {
      formData.append('student_id', grammar.student_id);
    }
    if (grammar.level) {
      formData.append('level', grammar.level);
    }
    formData.append('file', imageBlob, 'image.jpg');

    return this.api.post(`grammar/check`, formData).pipe(
      map((response) => {
        return response;
      })
    );
  }
}
