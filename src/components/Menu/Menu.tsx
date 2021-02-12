import React from 'react';
import './menu.css'
import TasksIcon from  './../../img/tasks.png'
import SolutionsIcon from './../../img/solutions.png'
import PasswordIcon from './../../img/password.png'
import GroupsIcon from './../../img/groups.png'
import UsersIcon from './../../img/users.png'

type Props = {
    type: string
}

const Menu: React.FunctionComponent<Props> = ({ type }) => {
    return (
        <div className="menu">
            <nav>
                <a href='/dashboard/my-tasks' className="button">
                    <img src={TasksIcon} alt="TasksIcon"/>
                    <span>My tasks</span>
                </a>

                <a href='/dashboard/my-solutions' className="button">
                    <img src={SolutionsIcon} alt="SolutionsIcon"/>
                    <span>My solutions</span>
                </a>

                <a href='/dashboard/change-password' className="button">
                    <img src={PasswordIcon} alt="PasswordIcon"/>
                    <span>Change password</span>
                </a>

                { (type === 'admin' || type === 'root') &&
                    <a href='/dashboard/tasks' className="button">
                        <img src={TasksIcon} alt="TasksIcon"/>
                        <span>Student's tasks</span>
                    </a>
                }

                { type === 'root' &&
                    <>
                        <a href='/dashboard/groups' className="button">
                            <img src={GroupsIcon} alt="GroupsIcon"/>
                            <span>Groups</span>
                        </a>

                        <a href='/dashboard/users' className="button">
                            <img src={UsersIcon} alt="UsersIcon"/>
                            <span>Users</span>
                        </a>
                    </>
                }
            </nav>
        </div>
    )
}

export default Menu;