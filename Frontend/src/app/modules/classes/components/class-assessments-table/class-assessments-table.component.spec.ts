import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ClassAssessmentsTableComponent } from './class-assessments-table.component';

describe('ClassAssessmentsTableComponent', () => {
  let component: ClassAssessmentsTableComponent;
  let fixture: ComponentFixture<ClassAssessmentsTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ClassAssessmentsTableComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ClassAssessmentsTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
