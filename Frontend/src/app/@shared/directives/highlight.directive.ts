import { Directive, ElementRef, EventEmitter, Input, OnChanges, Output, Renderer2 } from '@angular/core';
import { GrammarError } from '../../modules/assessments/models/grammar.model';

@Directive({
  selector: '[wlkHighlight]',
  standalone: false
})
export class HighlightDirective implements OnChanges {
  @Input() highlightText: string = ''; // Texto completo a analizar
  @Input() grammarErrors: GrammarError[] = []; // Lista de errores gramaticales

  @Output() openTooltip = new EventEmitter<GrammarError>();

  constructor(private el: ElementRef, private renderer: Renderer2) { }

  ngOnChanges() {
    this.renderer.setProperty(this.el.nativeElement, 'innerHTML', '');

    if (this.highlightText && this.grammarErrors.length > 0) {
      const fragment = document.createDocumentFragment();
      let lastIndex = 0;

      // Sort errors by position to process in order
      const sortedErrors = this.grammarErrors.sort((a, b) =>
        this.highlightText.indexOf(a.error_text) - this.highlightText.indexOf(b.error_text)
      );

      sortedErrors.forEach((error) => {
        const index = this.highlightText.indexOf(error.error_text, lastIndex);

        if (index > -1) {
          // Add text before error
          const before = this.highlightText.slice(lastIndex, index);
          fragment.appendChild(document.createTextNode(before));

          // Create highlighted span
          const span = this.renderer.createElement('span');
          this.renderer.addClass(span, 'highlight');
          this.renderer.setStyle(span, 'cursor', 'pointer');
          this.renderer.listen(span, 'click', () => {
            this.openTooltip.emit(error);
          });
          const errorText = this.renderer.createText(error.error_text);
          this.renderer.appendChild(span, errorText);
          fragment.appendChild(span);

          lastIndex = index + error.error_text.length;
        }
      });

      // Add remaining text
      const remaining = this.highlightText.slice(lastIndex);
      fragment.appendChild(document.createTextNode(remaining));

      // Append to the DOM
      this.renderer.appendChild(this.el.nativeElement, fragment);
    } else {
      this.renderer.setProperty(this.el.nativeElement, 'textContent', this.highlightText);
    }
  }


  private escapeRegExp(text: string): string {
    return text.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, '\\$&');
  }
}
