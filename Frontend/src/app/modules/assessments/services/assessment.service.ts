import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../../environments/environment';
import { Institution } from '../../shared/models/institutions.enum';
import { ExamType } from '../../shared/models/exam_type.enum';
import { Level } from '../../users/models/user-level.enum';
import { WritingTask } from '../models/writing.task.model';
import { ListAssessment } from '../models/list_assessment.model';
import { Assessment } from '../../assessments/models/assessment.model';
import { Writing, WritingAIFeedback } from '../models/writing.model';
import { Grammar } from '../models/grammar.model';
import { AssessmentsPolling } from '../models/assessments.pooling.started.model';
@Injectable({
    providedIn: 'root'
})
export class AssessmentService {
    private apiUrl = `${environment.apiUrl}/assessments`;

    constructor(private http: HttpClient) { }

    createAssessment(title: string, class_id: string, institution: Institution, exam_type: ExamType, level: Level, task: WritingTask, imageBlob: Blob): Observable<Assessment> {


        const formData = new FormData();
        formData.append('title', title);
        formData.append('class_id', class_id);
        formData.append('institution', institution);
        formData.append('exam_type', exam_type);
        formData.append('level', level);
        formData.append('task', task);
        formData.append('file', imageBlob, 'image.jpg');
        return this.http.post<Assessment>(this.apiUrl, formData);
    }


    startAssessment(assessmentId: string): Observable<Assessment> {
        return this.http.post<Assessment>(`${this.apiUrl}/${assessmentId}/start`, {});
    }

    updateAssessmentText(assessmentId: string, text: string): Observable<Assessment> {
        return this.http.patch<Assessment>(`${this.apiUrl}/${assessmentId}/text`, { text: text });
    }

    getAssessmentsByClassId(classId: string): Observable<Assessment[]> {
        return this.http.get<Assessment[]>(`${this.apiUrl}/class/${classId}`);
    }


    getAssessmentWritings(assessmentId: string): Observable<Writing[]> {
        return this.http.get<Writing[]>(`${this.apiUrl}/${assessmentId}/writings`);
    }


    updateWritingAIFeedback(assessmentId: string, writingId: string, aiFeedback: WritingAIFeedback): Observable<WritingAIFeedback> {
        return this.http.patch<WritingAIFeedback>(`${this.apiUrl}/${assessmentId}/writing/${writingId}/ai-feedback`, aiFeedback);
    }


    updateAssessmentGrammarFeedback(assessmentId: string, writingId: string, grammarFeedback: Grammar): Observable<Grammar> {
        return this.http.patch<Grammar>(`${this.apiUrl}/${assessmentId}/writing/${writingId}/grammar`, grammarFeedback);
    }

    listAssessments(limit: number = 10, offset: number = 0, isActive?: boolean, search?: string): Observable<ListAssessment> {
        let params = new HttpParams()
            .set('limit', limit.toString())
            .set('offset', offset.toString())

        if (isActive !== undefined) {
            params = params.set('is_active', isActive.toString());
        }

        if (search) {
            params = params.set('search', search);
        }

        return this.http.get<ListAssessment>(this.apiUrl, { params });
    }

    getAssessment(assessmentId: string): Observable<Assessment> {
        return this.http.get<Assessment>(`${this.apiUrl}/${assessmentId}`);
    }

    getStartedAssessments(): Observable<AssessmentsPolling> {
        return this.http.get<AssessmentsPolling>(`${this.apiUrl}/pooling/started`);
    }

    getAssessmentPoolingFinished(assessmentId: string): Observable<Assessment> {
        return this.http.get<Assessment>(`${this.apiUrl}/${assessmentId}/pooling/finished`);
    }

    updateAssessment(assessmentId: string, assessmentData: Assessment): Observable<Assessment> {
        return this.http.put<Assessment>(`${this.apiUrl}/${assessmentId}`, assessmentData);
    }

    activeAssessments(): Observable<Assessment> {
        return this.http.get<Assessment>(`${this.apiUrl}/active`, {});
    }


    uploadAssessmentWriting(assessmentId: string, studentId: string, files: Blob[]): Observable<Assessment> {
        const formData = new FormData();
        formData.append('student_id', studentId);
        files.forEach(file => {
            formData.append('files', file, 'image.jpg');
        });
        return this.http.put<Assessment>(`${this.apiUrl}/${assessmentId}/writing`, formData);
    }
} 