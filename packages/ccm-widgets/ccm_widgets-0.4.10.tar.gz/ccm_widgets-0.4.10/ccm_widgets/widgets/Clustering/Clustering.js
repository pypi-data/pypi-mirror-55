import React, { Component, useState } from 'react';
import { PythonInterface } from 'reactopya';
import { Grid, Paper, Table, TableHead, TableBody, TableRow, TableCell, Button } from '@material-ui/core'
import CanvasWidget, { CanvasWidgetLayer, PainterPath } from '../jscommon/CanvasWidget';
import { FormControl, Select, MenuItem, makeStyles, InputLabel, TextField } from '@material-ui/core';
import generateColorTable from './generateColorTable';
const ReactMarkdown = require('react-markdown');
const config = require('./Clustering.json');

export default class Clustering extends Component {
    static title = 'Evaluate clustering algorithms'
    static reactopyaConfig = config
    constructor(props) {
        super(props);
        this.state = {
            // javascript state
            alg_name: null,
            alg_arguments: null,
            kachery_config: null,

            // python state
            datasets: {datasets: []},
            algorithms: [],
            status: '',
            status_message: '',

            selectedAlgName: null,
            selectedAlgArguments: null
        }
    }
    componentDidMount() {
        this.pythonInterface = new PythonInterface(this, config);
        this.pythonInterface.start();
        this.setState({
            status: 'started',
            status_message: 'Starting python backend'
        });
        // Use this.pythonInterface.setState(...) to pass data to the python backend
        this.pythonInterface.setState({
            alg_name: 'none',
            alg_arguments: {},
            kachery_config: this.props.kachery_config || null
        });
    }
    componentWillUnmount() {
        this.pythonInterface.stop();
    }
    _clearData() {
        let datasets = this.state.datasets || {};
        for (let ds of datasets.datasets) {
            ds.data = null;
        }
        this.setState({
            datasets: datasets
        });
    }
    _handleUpdate = () => {
        this._clearData();
        this.pythonInterface.setState({
          alg_name: this.state.selectedAlgName,
          alg_arguments: this.state.selectedAlgArguments  
        });
    }
    render() {
        return (
            <ClusteringWidget
                loaded={this.state.status == 'finished'}
                statusText={this.state.status == 'finished' ? 'ready' : this.state.status_message}
                datasets={this.state.datasets}
                algorithms={this.state.algorithms}
                algorithmArguments={this.state.selectedAlgArguments || {}}
                algName={this.state.selectedAlgName || ''}
                // onChange={(algName, algorithmArguments) => {this._clearData(); this.pythonInterface.setState({alg_name: algName, alg_arguments: algorithmArguments})}}
                onChange={(algName, algorithmArguments) => {this.setState({selectedAlgName: algName, selectedAlgArguments: algorithmArguments})}}
                onUpdate={this._handleUpdate}
            />
        )
    }
}

function ClusteringWidget(props) {
    const { datasets, algorithms, algName, algorithmArguments } = props;
    if (!datasets) return <span />;
    if (!algorithms) return <span />;
    let itemStyle = {
        minWidth: 500
    };
    const style0 = {
        padding: 20
    };
    const _handleAlgorithmArgumentChanged = (name, val) => {
        let aa = algorithmArguments;
        aa[algName] = aa[algName] || {};
        aa[algName][name] = val;
        props.onChange(algName, aa);
    }
    return (
        <div style={style0}>
            <Overview />
            <div>Status: {props.statusText}</div>
            <AlgSelect
                disabled={!props.loaded}
                algorithms={algorithms}
                algorithmArguments={algorithmArguments}
                algName={algName}
                onAlgorithmArgumentChanged={_handleAlgorithmArgumentChanged}
                onAlgNameChanged={(name) => {props.onChange(name, algorithmArguments);}}
                onUpdate={() => {props.onUpdate();}}
            />
            <Grid container>
                {
                    datasets.datasets.map((ds) => (
                        <Grid item key={ds.name} style={itemStyle}>
                            {
                                <Dataset dataset={ds} />
                            }
                            
                        </Grid>
                    ))
                }
            </Grid>
        </div>
    )
}

function AlgSelect(props) {
    const { algorithms, algName, algorithmArguments, disabled } = props;
    if (!algorithmArguments) return <span />;
    let formFields = [
        {
            key: 'algName',
            label: 'Select clustering algorithm',
            type: 'select',
            value: algName,
            disabled: disabled,
            options: algorithms.map((alg) => (
                {
                    value: alg.name,
                    label: alg.label
                }
            ))
        }
    ];
    const _handleFieldChange = (key, val) => {
        if (key === 'algName') {
            props.onAlgNameChanged(val)
        }
        else {
            props.onAlgorithmArgumentChanged(key, val);
        }
    }
    let algorithm;
    for (let alg of algorithms) {
        if (alg.name === algName)
            algorithm = alg;
    }
    if (algorithm) {
        let aa = algorithmArguments[algName] || {};
        for (let param of algorithm.parameters) {
            if (aa[param.name] === undefined) {
                if (param.default !== undefined) {
                    _handleFieldChange(param.name, param.default);
                }
            }
            formFields.push({
                key: param.name,
                label: param.name,
                type: 'select',
                value: aa[param.name] === undefined ? param.default : aa[param.name],
                disabled: disabled,
                options: param.choices.map((choice) => (
                    {
                        value: choice,
                        label: choice
                    }
                ))
            });
        }
    }
    formFields.push({
        key: 'update',
        label: 'Update',
        type: 'button',
        onClick: () => {props.onUpdate();}
    })
    return (
        <div style={{ maxWidth: 300 }}>
            <Form2
                formFields={formFields}
                onFieldChange={_handleFieldChange}
            />
        </div>
    )
}

const useStyles = makeStyles(theme => ({
    root: {
        display: 'flex',
        flexDirection: 'column'
    },
    formControl: {
        margin: theme.spacing(1),
        minWidth: 120,
    },
    selectEmpty: {
        marginTop: theme.spacing(2),
    },
}));


function Form2(props) {
    const classes = useStyles();
    const { formFields } = props;
    return (
        <form className={classes.root} autoComplete="off">
            {
                formFields.map((ff) => (
                    <FormControl2
                        formField={ff}
                        key={ff.key}
                        onChange={(newval) => { props.onFieldChange && props.onFieldChange(ff.key, newval) }}
                    />
                ))
            }
        </form>
    )
}

class FormControl2 extends Component {
    render() {
        const { formField } = this.props;
        if (formField.type == 'select') {
            return (
                <FormControl key={formField.key}>
                    <InputLabel key="label" htmlFor={formField.key}>{formField.label}</InputLabel>
                    <Select key="select"
                        value={formField.value}
                        onChange={(evt) => { this.props.onChange(evt.target.value) }}
                        inputProps={{
                            name: formField.key,
                            id: formField.key,
                        }}
                        disabled={formField.disabled || false}
                    >
                        {
                            formField.options.map((option) => (
                                <MenuItem key={option.label} value={option.value}>{option.label}</MenuItem>
                            ))
                        }
                    </Select>
                </FormControl>
            );
        }
        else if (formField.type == 'float') {
            return (
                <TextField
                    id={formField.key}
                    label={formField.label}
                    value={formField.value}
                    onChange={(evt) => { this.props.onChange(Number(evt.target.value)) }}
                    // onChange={...}
                    type="number"
                />
            );
        }
        else if (formField.type == 'button') {
            return (
                <Button onClick={formField.onClick}>
                    {formField.label}
                </Button>
            );
        }
        else {
            return <span>Unknown type: {formField.type}</span>;
        }
    }
}

function Overview(props) {
    const markdown = `
# Clustering demo

These datasets have been downloaded from the [ClustEval](https://clusteval.sdu.dk/1/mains) website.

This application was created using [Reactopya](https://github.com/flatironinstitute/reactopya).
`;

    function linkRenderer(props) {
        return <a href={props.href} target="_blank">{props.children}</a>
    }

    return (
        <ReactMarkdown
            source={markdown}
            renderers={{ link: linkRenderer }}
        />
    );
}

function Dataset(props) {
    const { dataset } = props;
    let data2 = [];
    if (dataset.data) {
        for (let d of dataset.data) {
            data2.push({
                x: d[1],
                y: d[2]
            });
        }
    }
    return (
        <Paper>
            <h3>{dataset.name}</h3>
            <Table>
                <TableBody>
                    <TableRow>
                        <TableCell>URL</TableCell>
                        <TableCell><a href={dataset.url} target="_blank">{dataset.url}</a></TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell>Num. points</TableCell>
                        <TableCell>{data2.length}</TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell>Algorithm</TableCell>
                        <TableCell>{dataset.algName}</TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell>Elapsed (sec)</TableCell>
                        <TableCell>{dataset.elapsed || ''}</TableCell>
                    </TableRow>
                </TableBody>
            </Table>
            {
                dataset.data ? (
                    <Plot
                        data={data2}
                        labels={dataset.labels}
                    />
                ) : <span />
            }
            {/* <pre>
                {JSON.stringify(dataset, null, 4)}
            </pre> */}
        </Paper>
    )
}

class Plot extends Component {
    constructor(props) {
        super(props);
        this._mainLayer = new CanvasWidgetLayer(this._paintMainLayer);

        this._allLayers = [
            this._mainLayer
        ];
    }
    componentDidUpdate() {
        // this probably should not be necessary
        this._mainLayer.repaint();
    }
    _paintMainLayer = (painter) => {
        const { data, labels } = this.props;
        let W = this._mainLayer.width();
        let H = this._mainLayer.height();

        this._mainLayer.setCoordXRange(this._computeXRange());
        this._mainLayer.setCoordYRange(this._computeYRange());
        this._mainLayer.setPreserveAspectRatio(true);
        this._mainLayer.setMargins(20, 20, 20, 20);

        painter.useCoords();

        for (let i=0; i<data.length; i++) {
            let d = data[i];
            let label = labels ? labels[i] : 1;
            painter.setPen({ color: 'black' });
            painter.setBrush({ color: colorForLabel(label) });
            painter.drawMarker(d.x, d.y, 4, 'circle', {});
            painter.fillMarker(d.x, d.y, 4, 'circle', {});
        }
    }
    _computeXRange() {
        const { data } = this.props;
        let min = NaN;
        let max = NaN;
        for (let d of data) {
            if ((isNaN(min)) || (d.x <= min))
                min = d.x;
            if ((isNaN(max)) || (d.x >= max))
                max = d.x;
        }
        return [min, max];
    }
    _computeYRange() {
        const { data } = this.props;
        let min = NaN;
        let max = NaN;
        for (let d of data) {
            if ((isNaN(min)) || (d.y <= min))
                min = d.y;
            if ((isNaN(max)) || (d.y >= max))
                max = d.y;
        }
        return [min, max];
    }
    render() {
        let width = this.props.width || 400;
        let height = this.props.height || 400;
        return (
            <CanvasWidget
                layers={this._allLayers}
                width={width}
                height={height}
                menuOpts={{ exportSvg: true }}
            />
        );
    }
}

const colorTable = generateColorTable();

function colorForLabel(label) {
    if ((isNaN(Number(label))) || (label < 0)) {
        return 'white';
    }
    return colorTable[label % colorTable.length];
}

class RespectStatus extends Component {
    state = {}
    render() {
        switch (this.props.status) {
            case 'started':
                return <div>Started: {this.props.status_message}</div>
            case 'running':
                return <div>{this.props.status_message}</div>
            case 'error':
                return <div>Error: {this.props.status_message}</div>
            case 'finished':
                return this.props.children;
            default:
                return <div>Unknown status: {this.props.status}</div>
        }
    }
}