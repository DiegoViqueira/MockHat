import { inject, Injectable } from '@angular/core';
import { AssessmentService } from './assessment.service';
import { AssessmentState } from '../models/assessment.state.model';
import { Observable, finalize, interval, switchMap, takeWhile, tap } from 'rxjs';
import { Assessment } from '../models/assessment.model';
import { AssessmentStore } from '../stores/assessment.store';
import { MatSnackBar } from '@angular/material/snack-bar';
import { TOAST_OPTION, ToastService } from '../../../@core/services/toast.service';

@Injectable({
    providedIn: 'root'
})
export class AssessmentPollingService {
    private readonly POLLING_INTERVAL = 5000; // 5 segundos
    activePolling = new Set<string>();

    store = inject(AssessmentStore);
    snackBar = inject(MatSnackBar);
    assessmentService = inject(AssessmentService);
    toastService = inject(ToastService);


    constructor() {

        interval(this.POLLING_INTERVAL).pipe(
            switchMap(() => this.assessmentService.getStartedAssessments()),
            tap(assessments => {

                if (assessments.count > 0) {
                    assessments.assessments.forEach(id => {
                        if (!this.activePolling.has(id)) {
                            this.activePolling.add(id);
                            this.pollAssessmentState(id).subscribe({
                                error: (error) => {
                                    console.error(error);
                                    this.activePolling.delete(id);
                                },
                                complete: () => {
                                    this.activePolling.delete(id);
                                }
                            });
                        }
                    });
                }
            }



            )
        ).subscribe({
            error: (error) => {
                console.error(error);
            }
        });

    }

    private pollAssessmentState(assessmentId: string): Observable<Assessment> {
        return interval(this.POLLING_INTERVAL).pipe(
            switchMap(() => this.assessmentService.getAssessmentPoolingFinished(assessmentId)),
            takeWhile(assessment => assessment.state === AssessmentState.STARTED, true),
            tap(assessment => {

                if (assessment) {
                    if (assessment.state !== AssessmentState.STARTED) {
                        this.toastService.display(TOAST_OPTION.SUCCESS, 'OK', `Assessment [${assessment.title}] Finished`); 0
                        this.store.updateAssessmentState(assessment);
                    }
                }
            }),
            finalize(() => {
                this.activePolling.delete(assessmentId);
            })
        );
    }
} 