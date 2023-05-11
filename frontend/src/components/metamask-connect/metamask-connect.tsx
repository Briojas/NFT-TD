import styles from './metamask-connect.module.scss';
import classNames from 'classnames';

export interface MetamaskConnectProps {
    className?: string;
}

/**
 * This component was created using Codux's Default new component template.
 * To create custom component templates, see https://help.codux.com/kb/en/article/configuration-for-metamask-connects-and-templates
 */
export const MetamaskConnect = ({ className }: MetamaskConnectProps) => {
    return (
        <div className={classNames(styles.root, className)}>
            <button>Connect</button>
        </div>
    );
};
