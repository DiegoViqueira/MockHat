import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Class } from '../models/class.model';
import { environment } from '../../../../environments/environment';
import { Student } from '../../students/models/student.model';
import { ClassMetrics } from '../models/class.metrics.model';
import { ClassAnalysis } from '../models/class.analysis.model';


interface ListClass {
    classes: Class[];
    total: number;
}

@Injectable({
    providedIn: 'root'
})
export class ClassService {
    private apiUrl = `${environment.apiUrl}/classes`;

    constructor(private http: HttpClient) { }

    createClass(classData: Class): Observable<Class> {
        return this.http.post<Class>(this.apiUrl, classData);
    }

    getClassAnalysis(classId: string): Observable<ClassAnalysis> {
        return this.http.get<ClassAnalysis>(`${this.apiUrl}/${classId}/analysis`);
    }

    listClasses(limit: number = 10, offset: number = 0, isActive?: boolean, search?: string): Observable<ListClass> {
        let params = new HttpParams()
            .set('limit', limit.toString())
            .set('offset', offset.toString())

        if (isActive !== undefined) {
            params = params.set('is_active', isActive.toString());
        }

        if (search) {
            params = params.set('search', search);
        }

        return this.http.get<ListClass>(this.apiUrl, { params });
    }

    getClass(classId: string): Observable<Class> {
        return this.http.get<Class>(`${this.apiUrl}/${classId}`);
    }


    updateClass(classId: string, classData: Class): Observable<Class> {
        return this.http.put<Class>(`${this.apiUrl}/${classId}`, classData);
    }

    activeClasses(): Observable<Class> {
        return this.http.get<Class>(`${this.apiUrl}/active`, {});
    }

    getStudents(classId: string): Observable<Student[]> {
        return this.http.get<Student[]>(`${this.apiUrl}/${classId}/students`);
    }

    getClassMetrics(classId: string): Observable<ClassMetrics> {
        return this.http.get<ClassMetrics>(`${this.apiUrl}/${classId}/metrics`);
    }


} 