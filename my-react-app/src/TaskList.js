// src/TaskList.js
import React from 'react';
import Task from './Task';

const TaskList = ({ tasks }) => {
  return (
    <div className="task-list">
      <h2>Task List</h2>
      {tasks.map(task => (
        <Task key={task.id} task={task} />
      ))}
    </div>
  );
};

export default TaskList;
