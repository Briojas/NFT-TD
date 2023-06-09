import type React from 'react';
import { Card, Icon } from '@blueprintjs/core';
import classNames, { Value } from 'classnames';
import styles from './tower-card.module.scss';
import { useState, useEffect, useMemo } from 'react';
import { BlueprintIcons_16 } from '@blueprintjs/icons/lib/esm/generated-icons/16px/blueprint-icons-16';

export interface TowerData {
    tier: number;
    priority: number;
    operator: number;
    data1: number;
    data2: number;
    data3: number;
}

export interface TowerCardProps {
    tower?: TowerData;
    children?: React.ReactNode;
    className?: string;
}

export const TowerCard = ({ className, tower }: TowerCardProps) => {
    const operators = [
        BlueprintIcons_16['Divide'],
        BlueprintIcons_16['Cross'],
        BlueprintIcons_16['Minus'],
        BlueprintIcons_16['Plus'],
        // BlueprintIcons_16['Code'],
    ];

    // const conditionals = [
    //     BlueprintIcons_16['LessThan'],
    //     BlueprintIcons_16['GreaterThan'],
    //     BlueprintIcons_16['Slash'],
    // ];
    // const [isConditional, setIsConditional] = useState(false);

    const [operator, setOperator] = useState(tower?.operator || 0);
    if (operator < 0) {
        setOperator(0);
    } else if (operator > operators.length - 1) {
        setOperator(operators.length - 1);
    }

    const [data1, setData1] = useState(tower?.data1 || 2);
    const [data2, setData2] = useState(tower?.data2 || 11);
    const [data3, setData3] = useState(tower?.data3 || 5);

    var data1Name = 'Power';
    var data2Name = 'Range';
    var data3Name = 'Rate';

    // if (operator === operators[2] || operator === operators[3]) {
    //     data2Name = 'Splash';
    //     data3Name = 'Radius';
    // }
    // useEffect(() => {
    //     if (operator === operators[4]) {
    //         setIsConditional(true);
    //     }
    // }, [operator, operators]);

    return (
        <Card className={classNames(styles['wrapper'], className)}>
            <Card className={styles['tower']}>
                <div className={styles['card-id']}>
                    <p className={styles['tier']}>{'T' + tower?.tier}</p>
                    <div className={styles['priority-operator-selector']}>
                        <button
                            className={styles.adjustor}
                            onClick={() => setOperator(operator - 1)}
                        >
                            <Icon icon="caret-left" size={10} />
                        </button>
                    </div>
                    <Icon icon={operators[operator]} size={14} className={styles.operator} />
                    <div className={styles['priority-operator-selector']}>
                        <button
                            className={styles.adjustor}
                            onClick={() => setOperator(operator + 1)}
                        >
                            <Icon icon="caret-right" size={10} />
                        </button>
                    </div>
                    <p className={styles['priority']}>{'P' + tower?.priority}</p>
                </div>
                {/* {isConditional ? (
                    <div className={styles['card-data']}>
                        <div className={styles.data}>
                            <div className={styles['power-selector']}>
                                <button className={classNames(styles.plus, styles.adjustor)}>
                                    <Icon icon="caret-left" size={6} />
                                </button>
                            </div>
                            <div className={styles['power-selector']}>
                                <input
                                    type="number"
                                    value={data1}
                                    onChange={(e) => setData1(parseInt(e.target.value))}
                                />
                            </div>
                            <div className={styles['power-selector']}>
                                <button className={classNames(styles.plus, styles.adjustor)}>
                                    <Icon icon="caret-right" size={6} />
                                </button>
                            </div>
                        </div>
                        <div className={styles.data}>
                            <div className={styles['power-selector']}>
                                <button className={classNames(styles.plus, styles.adjustor)}>
                                    <Icon icon="caret-left" size={6} />
                                </button>
                            </div>
                            <div className={styles['power-selector']}>
                                <input
                                    type="number"
                                    value={data2}
                                    onChange={(e) => setData2(parseInt(e.target.value))}
                                />
                            </div>
                            <div className={styles['power-selector']}>
                                <button className={classNames(styles.plus, styles.adjustor)}>
                                    <Icon icon="caret-right" size={6} />
                                </button>
                            </div>
                        </div>
                    </div>
                ) : ( */}
                <div className={styles['card-data']}>
                    <div className={classNames(styles.product_row, styles.data)}>
                        <p>{data1Name}</p>
                        <input
                            type="number"
                            value={data1}
                            min={0}
                            max={99}
                            className={styles['data-value']}
                            onChange={(e) => setData1(parseInt(e.target.value))}
                        />
                    </div>
                    <div className={classNames(styles.product_row, styles.data)}>
                        <p>{data2Name}</p>
                        <input
                            type="number"
                            value={data2}
                            min={0}
                            max={99}
                            className={styles['data-value']}
                            onChange={(e) => setData2(parseInt(e.target.value))}
                        />
                    </div>
                    <div className={styles.data}>
                        <p>{data3Name}</p>
                        <input
                            type="number"
                            value={data3}
                            min={0}
                            max={99}
                            className={styles['data-value']}
                            onChange={(e) => setData3(parseInt(e.target.value))}
                        />
                    </div>
                </div>
                {/* )} */}
            </Card>
        </Card>
    );
};
