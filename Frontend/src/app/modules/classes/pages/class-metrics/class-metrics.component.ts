import { Component, computed, effect, inject, signal } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ClassStore } from '../../stores/class.store';
import { AppRoutes } from '../../../../@core/auth/models/routes.enum';
import { ClassService } from '../../services/class.service';
import { ClassMetrics } from '../../models/class.metrics.model';
@Component({
  selector: 'wlk-class-metrics',
  templateUrl: './class-metrics.component.html',
  styleUrl: './class-metrics.component.scss',
  standalone: false,
})
export class ClassMetricsComponent {
  store = inject(ClassStore);
  router = inject(Router);
  route = inject(ActivatedRoute);
  class = computed(() => this.store.class());
  classService = inject(ClassService);
  metrics = signal<ClassMetrics | null>(null);

  datasets: Array<{ data: number[]; label: string; backgroundColor: string, borderColor: string }> = [];
  labels: string[] = [];
  datasetsCriteriaAverage: Array<{ data: number[]; label: string; backgroundColor: string, borderColor: string }> = [];
  labelsCriteriaAverage: string[] = [];
  toUrl = {
    route: [AppRoutes.Modules, AppRoutes.Classes]
  };


  getPassRate() {
    if (!this.metrics()) {
      return 0;
    }
    return Math.round(this.metrics()?.class_score_metrics?.pass_rate * 100) / 100;
  }

  getScoreTrendData() {
    if (!this.metrics()) {
      return [];
    }
    if (!this.metrics()?.score_trends) {
      return [];
    }

    const scores = Object.values(this.metrics()?.score_trends?.weekly_average_scores);
    this.datasets = [{ data: [...scores], label: 'Score', backgroundColor: '#590fd2', borderColor: '#590fd2', }];
    this.labels = Object.keys(this.metrics()?.score_trends?.weekly_average_scores);
  }

  getCriteriaAverageData() {
    if (!this.metrics()) {
      return [];
    }
    if (!this.metrics()?.criteria_average) {
      return [];
    }

    const criteriaAverage = Object.values(this.metrics()?.criteria_average.criteria_scores);
    this.datasetsCriteriaAverage = [{ data: [...criteriaAverage], label: 'Criteria Average', borderColor: '#590fd2', backgroundColor: '#590fd2' }];
    this.labelsCriteriaAverage = Object.keys(this.metrics()?.criteria_average.criteria_scores);
  }

  constructor() {
    effect(() => {
      this.classService.getClassMetrics(this.class()?._id).subscribe((metrics) => {
        this.metrics.set(metrics);
        this.getScoreTrendData();
        this.getCriteriaAverageData();
      });
    });
  }

}
