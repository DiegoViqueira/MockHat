import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ClassMetricsComponent } from './class-metrics.component';

describe('ClassMetricsComponent', () => {
  let component: ClassMetricsComponent;
  let fixture: ComponentFixture<ClassMetricsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ClassMetricsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ClassMetricsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
