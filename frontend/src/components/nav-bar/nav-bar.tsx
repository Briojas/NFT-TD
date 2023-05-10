import styles from './nav-bar.module.scss';
import classNames from 'classnames';

export interface NavBarProps {
    className?: string;
}

/**
 * This component was created using Codux's Default new component template.
 * To create custom component templates, see https://help.codux.com/kb/en/article/configuration-for-nav-bars-and-templates
 */
export const NavBar = ({ className }: NavBarProps) => {
    return <div className={classNames(styles.root, className)}></div>;
};
