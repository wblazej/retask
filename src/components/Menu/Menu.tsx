import React from 'react';
import './menu.css'
import TasksIcon from  './../../img/tasks.png'
import SolutionsIcon from './../../img/solutions.png'
import PasswordIcon from './../../img/password.png'
import GroupsIcon from './../../img/groups.png'
import UsersIcon from './../../img/users.png'
import UserInfo from '../UserInfo/UserInfo';

const Menu = () => {
    return (
        <>
            <div className="menu">
                <div className="button">
                    <img src={TasksIcon} alt="TasksIcon"/>
                    <span>My tasks</span>
                </div>

                <div className="button">
                    <img src={SolutionsIcon} alt="SolutionsIcon"/>
                    <span>My solutions</span>
                </div>

                <div className="button">
                    <img src={PasswordIcon} alt="PasswordIcon"/>
                    <span>Change password</span>
                </div>

                <div className="button">
                    <img src={TasksIcon} alt="TasksIcon"/>
                    <span>Student's tasks</span>
                </div>

                <div className="button">
                    <img src={GroupsIcon} alt="GroupsIcon"/>
                    <span>Groups</span>
                </div>

                <div className="button">
                    <img src={UsersIcon} alt="UsersIcon"/>
                    <span>Users</span>
                </div>
            </div>
        </>
    )
}

export default Menu;