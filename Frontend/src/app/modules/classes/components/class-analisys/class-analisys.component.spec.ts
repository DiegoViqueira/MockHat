import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ClassAnalisysComponent } from './class-analisys.component';

describe('ClassAnalisysComponent', () => {
  let component: ClassAnalisysComponent;
  let fixture: ComponentFixture<ClassAnalisysComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ClassAnalisysComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ClassAnalisysComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
