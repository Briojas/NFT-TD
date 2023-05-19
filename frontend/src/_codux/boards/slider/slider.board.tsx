import { createBoard } from '@wixc3/react-board';
import { Slider } from '../../../components/slider/slider';

export default createBoard({
    name: 'Slider',
    Board: () => <Slider />
});
