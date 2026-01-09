import { Component, computed, effect, inject, signal } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Router } from '@angular/router';
import { ClassStore } from '../../stores/class.store';
import { ClassService } from '../../services/class.service';
import { AppRoutes } from '../../../../@core/auth/models/routes.enum';
import { ClassAnalysis } from '../../models/class.analysis.model';

@Component({
  selector: 'wlk-class-analisys',
  templateUrl: './class-analisys.component.html',
  styleUrl: './class-analisys.component.scss',
  standalone: false,

})
export class ClassAnalisysComponent {

  store = inject(ClassStore);
  router = inject(Router);
  route = inject(ActivatedRoute);
  class = computed(() => this.store.class());
  classService = inject(ClassService);
  analysis = signal<string | null>(null);


  toUrl = {
    route: [AppRoutes.Modules, AppRoutes.Classes]
  };

  constructor() {

    effect(() => {
      if (this.class()) {
        this.classService.getClassAnalysis(this.class()?._id).subscribe((analysis) => {
          this.analysis.set(analysis.summary);

        });
      }
    });
  }

}
