export interface Sprint {
  id: string; // '6738497cd0abd6989076bcd9';
  sprintName: string; // 'Спринт 2024.3.1.NPP Shared Sprint';
  sprintStatus: SprintStatus;
  sprintStartDate: string; // '2024-07-03T19:00:00';
  sprintEndDate: string; // '2024-07-16T19:00:00';
  entityIds: number[];
}

export type SprintStatus = 'Закрыт' | string;

export interface SprintDetail {
  id: string; //'6738497cd0abd6989076bcd9';
  sprintName: string; //'Спринт 2024.3.1.NPP Shared Sprint';
  sprintStatus: string; //'Закрыт';
  sprintStartDate: string; //'2024-07-03T19:00:00';
  sprintEndDate: string; //'2024-07-16T19:00:00';
  progress: number; //89.46236559139786;
  entities: SprintEntity[];
}

export interface SprintEntity {
  id: string; // '67399423c74a250499cc8238';
  entityId: string; // 4536835;
  area: string; // 'Система.Вики';
  type: string; // 'Дефект';
  status: string; // 'Закрыто';
  state: string; // 'Normal';
  priority: string; // 'Средний';
  ticketNumber: string; // 'PPWI-5523';
  name: string; // '[BE]  Некорректное выделение при добавлении инлайн-комментария ';
  createDate: string; // '2024-07-16T16:02:37.474230';
  createdBy: string; // 'В. К.';
  updateDate: string; // '2024-07-16T16:05:05.570567';
  updatedBy: string; // 'В. К.';
  parentTicketId: string; // null;
  assignee: string; // 'В. К.';
  owner: string; // 'А. М.';
  dueDate: string; // null;
  rank: string; // '0|qowcts:';
  estimation: string; // null;
  spent: number; // 28800;
  workgroup: string; // null;
  resolution: string; // 'Готово';
}
