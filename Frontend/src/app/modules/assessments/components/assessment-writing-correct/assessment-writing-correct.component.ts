import { Component, computed, effect, inject, Input, signal } from '@angular/core';
import { DeviceDetectionService } from '../../../../@core/services/device-detection.service';
import { ImageFile, ImageProcessorService } from '../../../../@shared/services/image-processor.service';
import { AssessmentStore } from '../../stores/assessment.store';
import { AssessmentService } from '../../services/assessment.service';
import { Assessment } from '../../models/assessment.model';
import { Class } from '../../../classes/models/class.model';
import { AssessmentState } from '../../models/assessment.state.model';
import { ClassStore } from '../../../classes/stores/class.store';
import { WritingState } from '../../models/writing.state.model';

@Component({
  selector: 'wlk-assessment-writing-correct',
  templateUrl: './assessment-writing-correct.component.html',
  styleUrl: './assessment-writing-correct.component.scss',
  standalone: false,
})
export class AssessmentWritingCorrectComponent {
  selectedElement: any;
  imageProcessor = inject(ImageProcessorService);
  device = inject(DeviceDetectionService);
  isMobile = this.device.isMobileScreen;
  displayedColumns: string[] = ['name', 'files', 'upload'];
  assessmentService = inject(AssessmentService);
  assessmentStore = inject(AssessmentStore);
  classStore = inject(ClassStore);

  isIOS = this.device.isIOS();

  assessment = computed(() => this.assessmentStore.assessment());
  class = computed(() => this.classStore.class());
  writings = computed(() => this.assessmentStore.writings());

  private filesMap = signal(new Map<string, ImageFile[]>());
  filesCount = computed(() => this.filesMap().size);

  isPending = signal(false);
  isCompleted = signal(false);

  constructor() {


    effect(() => {
      if (this.assessment) {
        this.assessmentStore.getAssessmentWritings(this.assessment()._id);
      }
    });

    effect(() => {
      if (this.assessment && this.assessment()?.state === AssessmentState.PENDING) {
        this.isPending.set(true);

      }
      else if (this.assessment && this.assessment()?.state === AssessmentState.COMPLETED) {
        this.isCompleted.set(true);
        this.isPending.set(false);
      } else if (this.assessment && this.assessment()?.state === AssessmentState.STARTED) {
        this.isPending.set(false);
        this.isCompleted.set(false);
      } else {
        this.isPending.set(false);
        this.isCompleted.set(false);
      }



    });
  }


  startAssessment() {

    this.assessmentService.startAssessment(this.assessment()._id).subscribe({
      next: (assessment) => {
        this.assessmentStore.setAssessment(assessment);
        this.isPending.set(false);
      },
      error: (error) => {
        console.error(error);
      }
    });
  }

  onFileChange(event: any, element: any) {

    const files = Array.from((event.target as HTMLInputElement).files || []);

    if (files) {
      this.imageProcessor.processImageFiles(files).then((imageFiles) => {
        this.assessmentStore.uploadAssessmentWriting(this.assessment()._id, element._id, imageFiles.map(file => file.file));
        this.updateFile(element._id, imageFiles);
      });
    }

    // const file = (event.target as HTMLInputElement).files?.[0];



    // if (file) {

    //   this.imageProcessor.processImageFile(file).then((imageFile) => {

    //     this.assessmentService.uploadAssessmentWriting(this.assessment()._id, element._id, imageFile.file).subscribe({
    //       next: (writing) => {
    //         this.updateFile(element._id, imageFile);
    //       },
    //       error: (error) => {
    //         console.error(error);
    //       }
    //     });


    //   });

    // }
  }

  // Método para actualizar el mapa
  updateFile(studentId: string, files: ImageFile[]) {
    this.filesMap.update(map => {
      const newMap = new Map(map);
      newMap.set(studentId, files);
      return newMap;
    });
  }

  isWritingUploaded(element: any) {

    if (this.writings()) {
      const writing = this.writings().find(writing => writing.student._id === element._id);
      if (writing && writing.writing_state !== WritingState.PENDING) {
        return true;
      }
    }


    return false;
  }

  // Método para obtener el archivo
  getStudentFiles(studentId: string) {


    const files = this.filesMap().get(studentId);
    if (files) {
      return files;
    }
    return [];
  }

  selectElement(element: any) {
    this.selectedElement = element;
  }



}
