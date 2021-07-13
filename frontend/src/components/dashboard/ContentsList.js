import React from 'react';
import { Pagination } from '@material-ui/lab';
import { Card, Divider, Grid, ImageListItem } from '@material-ui/core';
import { withStyles } from '@material-ui/core/styles';
import { Box, ImageList, ImageListItemBar } from '@material-ui/core';
import Typography from '@material-ui/core/Typography';
import ContentsListAPI from '../../helper/dashboard/ContentsListAPI';

const styles = (theme) => ({
  root: {
    width: '100%',
    backgroundColor: theme.palette.background.paper,
  },
  inline: {
    display: 'inline',
  },
});

class UsersList extends React.Component {
  constructor(props) {
    super(props);

    this.state = {};
    this.api = new ContentsListAPI();
  }

  componentDidMount() {
    this.api.call(
      contents => {
        this.setState({
          contents: contents
        });
      },
      err => {
        throw err;
      });
  }

  render() {
    const { classes } = this.props;
    const { contents } = this.state;
    const handlePaginate = (e, page) => {
      this.api.call(
        contents => {
          this.setState({
            contents: contents
          });
        },
        err => {
          throw err;
        },
        page);
    };
    if(contents) {
      return (
        <Box className={classes.root}>
          <Box m={2}>
            <Pagination 
              count={contents.pagination.total_pages}
              variant="outlined" 
              shape="rounded"
              onChange={handlePaginate} />
          </Box>
          <ImageList cols={4} gap={16} style={{bgcolor: "#000"}}>
            {
              contents.models.map(content => (
                <ImageListItem
                  key={content.id} 
                  component="a" 
                  href={'/app/new/' + content.id}>
                  <img
                    srcSet={`https://placehold.jp/640x480.png`}
                    alt={content.title}
                    loading="lazy"
                  />
                  <ImageListItemBar
                    title={content.title}
                    subtitle={<span>added by: {content.user.username}</span>}
                  />
                </ImageListItem>
              ))
            }
          </ImageList>
        </Box>
      );
    } else {
      return (
        <Card>
          <Box>
            LOAD DATA...
          </Box>
        </Card>
      );
    }
  };
};

export default withStyles(styles)(UsersList);
