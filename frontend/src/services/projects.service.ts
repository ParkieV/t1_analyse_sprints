import { Injectable } from '@angular/core';
import { Project } from '../models/project.model';

@Injectable({
  providedIn: 'root'
})
export class ProjectsService {
  activeProject: Project = {
    id: 'qwe123',
    name: 'Фронтенд'
  }

  constructor() { }
}
