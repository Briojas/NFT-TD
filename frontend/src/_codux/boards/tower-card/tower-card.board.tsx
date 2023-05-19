import { createBoard } from '@wixc3/react-board';
import { TowerCard } from '../../../components/tower-card/tower-card';

const divide = 'divide'
const multiply = 'cross'
const minus = 'minus'
const add = 'plus'
const conditional = 'code'

export default createBoard({
    name: 'TowerCard',
    Board: () => <TowerCard tier={1} operator={divide} priority={5} power={11}/>,
    environmentProps: {
        windowWidth: 375,
        windowHeight: 667,
        canvasWidth: 298,
    },
});
