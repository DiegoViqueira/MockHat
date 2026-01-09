import { Component } from '@angular/core';
import { AssessmentPollingService } from './services/assessment-polling.service';

@Component({
  selector: 'wlk-assessments',
  template: ` <router-outlet></router-outlet> `,
  standalone: false
})
export class AssessmentsComponent {

  constructor() {

  }
}
