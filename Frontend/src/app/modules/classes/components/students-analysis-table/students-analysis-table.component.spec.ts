import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StudentsAnalysisTableComponent } from './students-analysis-table.component';

describe('StudentsAnalysisTableComponent', () => {
  let component: StudentsAnalysisTableComponent;
  let fixture: ComponentFixture<StudentsAnalysisTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StudentsAnalysisTableComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(StudentsAnalysisTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
