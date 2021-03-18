import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NovoImovelComponent } from './novo-imovel.component';

describe('NovoImovelComponent', () => {
  let component: NovoImovelComponent;
  let fixture: ComponentFixture<NovoImovelComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NovoImovelComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(NovoImovelComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
