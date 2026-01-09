import { Component, computed, effect, inject, signal } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { ClassStore } from '../../../classes/stores/class.store';
import { ImageFile, ImageProcessorService } from '../../../../@shared/services/image-processor.service';
import { DeviceDetectionService } from '../../../../@core/services/device-detection.service';
import { ExamType } from '../../../shared/models/exam_type.enum';
import { WritingTask } from '../../models/writing.task.model';
import { AssessmentStore } from '../../stores/assessment.store';
import { getExamTypesByInstitution, getTasksByInstitutionExamTypeAndLevel } from '../../../../@shared/common-environment/common-environment';
import { AppRoutes } from '../../../../@core/auth/models/routes.enum';
import { Router } from '@angular/router';
@Component({
  selector: 'wlk-create-assessment',
  templateUrl: './create-assessment.component.html',
  styleUrl: './create-assessment.component.scss',
  standalone: false
})
export class CreateAssessmentComponent {
  private readonly deviceDetectionService = inject(DeviceDetectionService);
  protected readonly isMobile = computed(() => this.deviceDetectionService.isMobileScreen());
  isIOS = this.deviceDetectionService.isIOS();

  private store = inject(ClassStore);
  private assessmentStore = inject(AssessmentStore);
  class = computed(() => this.store.class());
  assessment = computed(() => this.assessmentStore.assessment());
  imageProcessor = inject(ImageProcessorService);
  imageFile = signal<ImageFile | undefined>(undefined);
  router = inject(Router);


  availableExamTypes: ExamType[] = [];
  availableTasks: WritingTask[] = [];


  private _fb = inject(FormBuilder);
  form = this._fb.group({
    name: ['', [Validators.required]],
    exam_type: [ExamType.CEQ, [Validators.required]],
    task: [WritingTask.EMAIL, [Validators.required]],
  });

  constructor() {

    if (this.class()) {
      this.availableExamTypes = getExamTypesByInstitution(this.class().institution);
      this.availableTasks = getTasksByInstitutionExamTypeAndLevel(this.class().institution, this.form.get('exam_type')?.value, this.class()?.level);
    }

    effect(() => {
      if (this.assessment()) {
        console.log('navigate to validate');
        this.router.navigate([AppRoutes.Modules, AppRoutes.Assessments, AppRoutes.ViewAssessment],
          {
            queryParams: { mode: 'validate' }
          }
        );
      }
    });
  }

  url = signal(undefined);
  backUrl: any = {
    route: [AppRoutes.Modules, AppRoutes.Classes, AppRoutes.Class],
    queryParams: { "to": 'assessments' }
  };


  onFileChange = async (event: any) => {
    const file = (event.target as HTMLInputElement).files?.[0];
    if (file) {
      this.imageProcessor.processImageFile(file).then((imageFile) => {
        this.imageFile.set(imageFile);
        this.url.set(imageFile.url);
      });
    }
  }

  createAssessment() {
    this.assessmentStore.create(this.form.get('name')?.value, this.class()._id, this.class().institution, this.form.get('exam_type')?.value, this.class().level, this.form.get('task')?.value, this.imageFile()?.file);
  }

  onExamTypeChange(selectedExamType: ExamType): void {

    if (this.class()) {
      this.form.get('exam_type')?.setValue(selectedExamType);

      // Obtener niveles disponibles para la institución y tipo de examen
      const selectedInstitution = this.class().institution;
      const selectedLevel = this.class().level;

      // Resetear y actualizar el nivel
      this.availableTasks = getTasksByInstitutionExamTypeAndLevel(selectedInstitution, selectedExamType, selectedLevel);
    }
  }

}
