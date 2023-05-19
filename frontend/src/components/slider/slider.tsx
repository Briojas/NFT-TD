import styles from './slider.module.scss';
import classNames from 'classnames';
import { Slider } from '@blueprintjs/core';

export interface JointSliderProps {
    className?: string;
}

/**
 * This component was created using Codux's Default new component template.
 * To create custom component templates, see https://help.codux.com/kb/en/article/configuration-for-sliders-and-templates
 */
export const JointSlider = ({ className }: JointSliderProps) => {
    return (
        <Slider
            className={classNames(styles.root, className)}
            min={0}
            max={10}
            stepSize={0.1}
            labelStepSize={10}
            vertical={true}
        />
    );
};
