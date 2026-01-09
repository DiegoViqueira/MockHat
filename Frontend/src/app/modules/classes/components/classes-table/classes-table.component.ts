import { Component, computed, effect, inject, EventEmitter, Output, signal } from '@angular/core';
import { Class } from '../../models/class.model';
import { ClassStore } from '../../stores/class.store';
import { DeviceDetectionService } from '../../../../@core/services/device-detection.service';

@Component({
  selector: 'wlk-classes-table',
  templateUrl: './classes-table.component.html',
  styleUrl: './classes-table.component.scss',
  standalone: false,
})
export class ClassesTableComponent {

  store = inject(ClassStore);

  device = inject(DeviceDetectionService);
  isMobile = this.device.isMobileScreen;


  classes = computed(() => this.store.classes());
  classesfiltered = signal<Class[]>([]);

  @Output() gotoClass = new EventEmitter<Class>();
  @Output() viewMetrics = new EventEmitter<Class>();
  @Output() viewClassAnalysis = new EventEmitter<Class>();



  classClick(element: Class) {
    this.gotoClass.emit(element);
  }

  constructor() {

    effect(() => {

      this.classesfiltered.set(this.classes());
    });
  }






  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.classesfiltered.set(this.classes().filter(_class => _class.name.toLowerCase().includes(filterValue.trim().toLowerCase())));
  }



}
