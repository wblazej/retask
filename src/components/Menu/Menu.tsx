import React from 'react';
import './menu.css'
import TasksIcon from  './../../img/tasks.png'
import SolutionsIcon from './../../img/solutions.png'
import PasswordIcon from './../../img/password.png'
import GroupsIcon from './../../img/groups.png'
import UsersIcon from './../../img/users.png'
import { Link } from 'react-router-dom';

type Props = {
    type: string
}

const Menu: React.FunctionComponent<Props> = ({ type }) => {
    return (
        <div className="menu">
            <nav>
                <Link to='/dashboard' className="button">
                    <img src={TasksIcon} alt="TasksIcon"/>
                    <span>My tasks</span>
                </Link>

                <Link to='/dashboard/my-solutions' className="button">
                    <img src={SolutionsIcon} alt="SolutionsIcon"/>
                    <span>My solutions</span>
                </Link>

                <Link to='/dashboard/change-password' className="button">
                    <img src={PasswordIcon} alt="PasswordIcon"/>
                    <span>Change password</span>
                </Link>

                { (type === 'admin' || type === 'root') &&
                    <Link to='/dashboard/tasks' className="button">
                        <img src={TasksIcon} alt="TasksIcon"/>
                        <span>Student's tasks</span>
                    </Link>
                }

                { type === 'root' &&
                    <>
                        <Link to='/dashboard/groups' className="button">
                            <img src={GroupsIcon} alt="GroupsIcon"/>
                            <span>Groups</span>
                        </Link>

                        <Link to='/dashboard/users' className="button">
                            <img src={UsersIcon} alt="UsersIcon"/>
                            <span>Users</span>
                        </Link>
                    </>
                }
            </nav>
        </div>
    )
}

export default Menu;