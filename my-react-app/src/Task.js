// src/Task.js
import React from 'react';

const Task = ({ task }) => {
  return (
    <div className="task">
      <h3>{task.title}</h3>
      <p>{task.description}</p>
      <p>Priority: {task.priority}</p>
    </div>
  );
};

export default Task;
