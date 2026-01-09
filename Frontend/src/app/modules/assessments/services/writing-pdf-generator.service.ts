import { Injectable } from '@angular/core';
import pdfMake from 'pdfmake/build/pdfmake';
import pdfFonts from 'pdfmake/build/vfs_fonts';
import { Writing, WritingCriteriaScore } from '../../assessments/models/writing.model';
import { Assessment } from '../models/assessment.model';
import { Class } from '../../classes/models/class.model';
import { GrammarError } from '../models/grammar.model';

pdfMake.vfs = pdfFonts.vfs;



@Injectable({
  providedIn: 'root'
})
export class WritingPdfGeneratorService {

  generatePdf(writing: Writing, assessment: Assessment, _class: Class): void {



    this.getBase64ImageFromURL('assets/images/mockhat.png').then((imageData) => {
      const documentDefinition = this.getDocumentDefinition(writing, assessment, _class, imageData);
      pdfMake.createPdf(documentDefinition).open();
    });
  }




  private getBase64ImageFromURL(url: string): Promise<string> {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.setAttribute('crossOrigin', 'anonymous');
      img.onload = () => {
        const canvas = document.createElement('canvas');
        canvas.width = img.width;
        canvas.height = img.height;
        const ctx = canvas.getContext('2d');
        ctx?.drawImage(img, 0, 0);
        const dataURL = canvas.toDataURL('image/png');
        resolve(dataURL);
      };
      img.onerror = (error) => {
        reject(error);
      };
      img.src = url;
    });
  }

  private getDocumentDefinition(writing: Writing, assessment: Assessment, _class: Class, imageData: string): any {
    return {
      pageMargins: [30, 80, 30, 40], // [izquierda, arriba, derecha, abajo]
      header: {
        margin: [40, 20, 40, 20], // margen para todo el header
        columns: [
          {
            image: imageData,
            width: 50,
            alignment: 'left',
            margin: [0, 0, 0, 0] // quitamos el margen individual del logo
          },
          {
            text: '', // columna vacía para empujar el logo a la izquierda
            width: '*'
          }
        ]
      },
      content: [
        { text: '\n Assessment Result', style: 'header' },
        { text: '\nTitle: ' + assessment.title, style: 'subheader' },
        { text: 'Class: ' + _class.name, style: 'subheader' },
        { text: 'Student: ' + writing.student.name + ' ' + writing.student.last_name, style: 'subheader' },
        { text: 'Score: ' + writing.ai_feedback.criterias.map((criteria: WritingCriteriaScore) => criteria.score).reduce((a, b) => a + b, 0), style: 'subheader' },
        { text: '\n' },
        { text: 'Assessment: ', margin: [0, 10, 0, 5], style: 'subheader' },
        {
          table: {
            widths: ['*'],
            body: [[
              { text: assessment.image_text, margin: [5, 5, 5, 5], fontSize: 10 }
            ]],
          },
          layout: {
            hLineWidth: () => 1,
            vLineWidth: () => 1,
            hLineColor: () => '#ddd',
            vLineColor: () => '#ddd',
          }
        },
        { text: '\n' },
        { text: 'Student Answer: ', margin: [0, 10, 0, 5], style: 'subheader' },
        {
          table: {
            widths: ['*'],
            body: [[
              { text: writing.student_response_text, margin: [5, 5, 5, 5], fontSize: 10 }
            ]],
          },
          layout: {
            hLineWidth: () => 1,
            vLineWidth: () => 1,
            hLineColor: () => '#ddd',
            vLineColor: () => '#ddd',
          }
        },
        { text: '\n' },
        { text: 'Evaluation Criterias', style: 'subheader' },
        {

          table: {
            widths: ['*', '*', '*'],
            body: [
              [
                { text: 'Criteria', fontSize: 10, bold: true, color: '#310872' },
                { text: 'Score', fontSize: 10, bold: true, color: '#310872' },
                { text: 'Feedback', fontSize: 10, bold: true, color: '#310872' }
              ],
              ...writing.ai_feedback.criterias.map((criteria: WritingCriteriaScore) => [
                { text: criteria.criteria, fontSize: 10 },
                { text: criteria.score, fontSize: 10 },
                { text: criteria.feedback, fontSize: 10 }
              ]),
            ],
            layout: {
              hLineWidth: () => 1,
              vLineWidth: () => 1,
              hLineColor: () => '#ddd',
              vLineColor: () => '#ddd',
            },
          },
        },

        { text: '\n' },
        { text: 'Grammatical Errors', style: 'subheader' },
        {

          table: {
            widths: ['*', '*', '*'],
            body: [
              [
                { text: 'Error', fontSize: 10, bold: true, color: '#310872' },
                { text: 'Corrected Text', fontSize: 10, bold: true, color: '#310872' },
                { text: 'Correction Explanation', fontSize: 10, bold: true, color: '#310872' }
              ],
              ...writing.grammar_feedback.errors.map((error: GrammarError) => [
                { text: error.error_text, fontSize: 10 },
                { text: error.corrected_text, fontSize: 10 },
                { text: error.correction_explanation, fontSize: 10 }
              ]),
            ],
            layout: {
              hLineWidth: () => 1,
              vLineWidth: () => 1,
              hLineColor: () => '#ddd',
              vLineColor: () => '#ddd',
            }
          },
        },
      ],
      styles: {
        header: {
          fontSize: 18,
          bold: true,
          margin: [0, 0, 0, 10],
          color: '#310872',
        },
        subheader: {
          fontSize: 14,
          bold: true,
          margin: [0, 0, 0, 5],
          color: '#310872',
        },
        tableHeader: {
          fontSize: 10,
          bold: true,
          margin: [5, 5, 5, 5]
        },
        tableCell: {
          fontSize: 10,
          margin: [5, 5, 5, 5]
        }
      },
    };
  }
}
