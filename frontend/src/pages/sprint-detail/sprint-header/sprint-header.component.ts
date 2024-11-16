import { Component } from '@angular/core';
import { DateSelectorComponent } from "../../../components/date-selector/date-selector.component";

@Component({
  selector: 'app-sprint-header',
  standalone: true,
  imports: [DateSelectorComponent],
  templateUrl: './sprint-header.component.html',
  styleUrl: './sprint-header.component.scss'
})
export class SprintHeaderComponent {

}
