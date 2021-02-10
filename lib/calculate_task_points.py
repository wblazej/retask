def calculete_task_points(solutions, tasks_count):
    points = []
    for i in range(tasks_count):
        s_count = 0
        for key in solutions.keys():
            if i + 1 in solutions[key]:
                s_count += 1
        
        if s_count == 0:
            points.append(100)
        else:
            points.append(round(100 / s_count))

    return points