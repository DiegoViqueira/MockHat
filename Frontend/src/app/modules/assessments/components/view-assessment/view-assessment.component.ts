import { Component, computed, effect, inject } from '@angular/core';
import { AssessmentStore } from '../../stores/assessment.store';
import { FormBuilder, Validators } from '@angular/forms';
import { DomSanitizer } from '@angular/platform-browser';
import { ActivatedRoute, Router } from '@angular/router';
import { ClassStore } from '../../../classes/stores/class.store';
import { AppRoutes } from '../../../../@core/auth/models/routes.enum';

@Component({
  selector: 'wlk-view-assessment',
  templateUrl: './view-assessment.component.html',
  styleUrl: './view-assessment.component.scss',
  standalone: false,
})
export class ViewAssessmentComponent {
  router = inject(Router);
  sanitizer = inject(DomSanitizer);
  route = inject(ActivatedRoute);
  mode = this.route.snapshot.queryParams['mode'];
  private _fb = inject(FormBuilder);
  store = inject(AssessmentStore);
  assessment = computed(() => this.store.assessment());
  classStore = inject(ClassStore);
  class = computed(() => this.classStore.class());


  form = this._fb.group({
    image_text: ['', [Validators.required]],
  });

  backUrl: any = {
    route: [AppRoutes.Modules, AppRoutes.Classes, AppRoutes.Class],
    queryParams: { "to": 'assessments' }
  };

  constructor() {
    effect(() => {
      if (this.assessment()) {
        this.form.patchValue({
          image_text: this.assessment()?.image_text,
        });
      }
    });
  }

  updateAssessmentText() {
    this.store.updateAssessmentText(this.assessment()?._id, this.form.value.image_text);
  }

  ok() {
    this.store.setAssessment(null);
    this.router.navigate([AppRoutes.Modules, AppRoutes.Classes, AppRoutes.Class], { queryParams: { "to": 'assessments' } });
  }

  back() {
    this.store.setAssessment(null);
  }
}
