import { createBoard } from '@wixc3/react-board';
import { TowerCard } from '../../../components/tower-card/tower-card';

const divide = 'divide'
const multiply = 'cross'
const minus = 'minus'
const add = 'plus'
const conditional = 'code'

const tier = 3
const operator = conditional
const priority = 5
const data1 = 'Less than'
const data2 = 45
const data3 = 99

export default createBoard({
    name: 'TowerCard',
    Board: () => <TowerCard tier={tier} operator={operator} priority={priority} data1={data1} data2={data2} data3={data3}/>,
    environmentProps: {
        windowWidth: 375,
        windowHeight: 667,
        canvasWidth: 298,
    },
});
